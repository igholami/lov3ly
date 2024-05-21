from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from webauthn import generate_registration_options, generate_authentication_options, verify_authentication_response


from webauthn import (
    generate_registration_options,
    options_to_json,
    verify_registration_response,
    base64url_to_bytes,

)
from webauthn.helpers.bytes_to_base64url import bytes_to_base64url
from webauthn.helpers.exceptions import InvalidRegistrationResponse
from webauthn.helpers.parse_authentication_credential_json import parse_authentication_credential_json
from webauthn.helpers.parse_registration_credential_json import parse_registration_credential_json
from webauthn.helpers.structs import (
    RegistrationCredential, PublicKeyCredentialDescriptor, AuthenticationCredential,
)

from .helpers import get_domain
from .models import *
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages, auth


def index(request):
    if request.user.is_authenticated:
        return home(request)
    return render(request, "auth.html")


def register(request, user):
    public_credential_creation_options = generate_registration_options(
        rp_id=get_domain(request),  # On dev make sure that you have the ports here
        rp_name=settings.WEBAUTHN_RP_NAME,
        user_name=user.email,
        user_id=bytes(str(user.pk), "utf-8"),
    )
    webauthn_registration, _ = WebauthnRegistration.objects.get_or_create(
        user=user
    )
    options_dict = json.loads(options_to_json(public_credential_creation_options))
    webauthn_registration.challenge = options_dict["challenge"]
    webauthn_registration.save()
    return render(
        request,
        "register.html",
        context={
            "public_credential_creation_options": options_to_json(
                public_credential_creation_options
            ),
            "email": user.email,
        },
    )


@require_POST
def complete_registration(request):
    data = json.loads(request.body)

    user = get_object_or_404(User, email=data["email"])
    webauthn_registration = WebauthnRegistration.objects.get(user=user)

    del data[("email")]
    registration_credentials = parse_registration_credential_json(data)

    try:
        verified_registration = verify_registration_response(
            credential=registration_credentials,
            expected_challenge=base64url_to_bytes(webauthn_registration.challenge),
            expected_origin=f"{settings.WEBAUTHN_METHOD}://{request.get_host()}",  # dont forget the ports
            expected_rp_id=get_domain(request),
        )

        WebauthnCredentials.objects.create(
            user=user,
            name=user.email,
            credential_public_key=bytes_to_base64url(verified_registration.credential_public_key),
            credential_id=bytes_to_base64url(verified_registration.credential_id),
        )

        auth.login(request, user)

        return HttpResponse(status=201)
    except InvalidRegistrationResponse as error:
        messages.error(
            request,
            f"Something went wrong: {error}",
        )
        return redirect("fingerprint")


def login(request, user):
    authenticators = user.webauthn.all()
    webauthn_authentication, _ = WebauthnAuthentication.objects.get_or_create(
        user=user
    )
    allowed_credentials = [
        PublicKeyCredentialDescriptor(
            id=base64url_to_bytes(credentials.credential_id)
        )
        for credentials in authenticators
    ]
    authentication_options = generate_authentication_options(
        rp_id=get_domain(request),
        allow_credentials=allowed_credentials,
    )
    json_option = json.loads(options_to_json(authentication_options))
    webauthn_authentication.challenge = json_option.get("challenge")
    webauthn_authentication.save()
    return render(
        request,
        "login.html",
        context={
            "authentication_options": options_to_json(authentication_options),
            "email": user.email,
        },
    )

@require_POST
def complete_login(request):
    data = json.loads(request.body)
    user = get_object_or_404(User, email=data["email"])
    webauthn_authentication = WebauthnAuthentication.objects.get(user=user)

    del data["email"]
    authentication_credential = parse_authentication_credential_json(data)
    webauthn_credentials = get_object_or_404(
        WebauthnCredentials,
        credential_id=authentication_credential.id
    )
    if webauthn_credentials.user != user:
        return HttpResponse(status=403)
    authentication_verification = verify_authentication_response(
        credential=authentication_credential,
        expected_challenge=base64url_to_bytes(webauthn_authentication.challenge),
        expected_rp_id=get_domain(request),
        expected_origin=f"{settings.WEBAUTHN_METHOD}://{request.get_host()}",
        credential_public_key=base64url_to_bytes(
            webauthn_credentials.credential_public_key
        ),
        credential_current_sign_count=webauthn_credentials.current_sign_count,
    )
    webauthn_credentials.current_sign_count = (
        authentication_verification.new_sign_count
    )
    auth.login(request, user)
    return HttpResponse(status=200)

def home(request):
    return render(
        request,
        "fingerprint_home.html",
        context={
            "user": request.user
        }
    )

@require_POST
def authenticate(request):
    user = User.objects.filter(email=request.POST["email"])
    if not user or WebauthnCredentials.objects.filter(user=user[0]).count() == 0:
        user = User.objects.get_or_create(
            email=request.POST["email"],
            username=request.POST["email"],
        )[0]
        return register(request, user)
    user = user[0]
    return login(request, user)

def logout(request):
    auth.logout(request)
    return redirect("fingerprint")