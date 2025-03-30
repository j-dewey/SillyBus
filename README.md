# SillyBus
Sillybus is a web application that allows users to upload their Syllabi and sync the due dates with their Google Calendar.

## Run It Yourself

### Dependencies
- django
- python-dotenv
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- convertapi
- tempfile

### Secrets Managments
Needed envimroment variablse include

- KETYFORCONVERT = <covert api key>
- KEYFORPERP = <perplexity ai api key>
- KEYFORDJANGO = <django api key>
- GOOGLECLIENTID = <client id from google>

## Interacting with Google Cloud

1. Create a [Google Cloud Project]<https://developers.google.com/workspace/guides/create-project>.
2. From the [API Library]<https://console.cloud.google.com/workspace-api/products> select your project, and enable the Google Tasks API.
3. Create a [service account]<https://cloud.google.com/iam/docs/service-account-overview> for interacting with a google product.
4. Now from the [Auth Platform Clients Page]<https://console.developers.google.com/auth/clients> enable the following:
- Authorized origin points:
  - https://\< host \>
  - https://\< host \>:8000
- Authorized redirect URI:
  - https://\< host \>:8000/auth-receiver
  - https://\< host \>:8000
  - https://\< host \>:50125
5. Finally, from **Data Access > Add or Remove Scope** extend scope to include Google Tasks.

## Use Case
A student uploads their syllabi and the due dates are synced with their Google Calendar. The alternative that many students face is manually adding the due dates to their calendar, which is time-consuming and error-prone as well as extremely boring.

