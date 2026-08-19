# AI integration modes

This repository is intentionally deployable as a static GitHub Pages site. It does not put OpenAI, HHS, CDC, or other service credentials in browser code.

## 1. Local Browser AI

The extended demo dynamically loads `@mlc-ai/web-llm` from its documented CDN entry point and selects a small supported instruct model. Model inference runs in the browser using WebGPU. The first model load may require a substantial download; browser caching normally improves repeat visits.

This mode is ideal for a public demonstration because it needs no application server and no API credential.

## 2. HHS/CDC approved gateway

The UI includes a gateway mode for a future, agency-approved HTTPS endpoint. The browser sends:

```json
{
  "messages": [{"role": "user", "content": "..."}],
  "source": "jupyterlite-data-visualization-demo"
}
```

with `credentials: "include"`, allowing an approved same-agency authentication design to rely on its browser session. The endpoint must explicitly allow the GitHub Pages origin through CORS and should enforce authentication/authorization server-side.

The demo accepts one of these JSON response forms:

```json
{"message":{"content":"..."}}
```

```json
{"output_text":"..."}
```

```json
{"response":"..."}
```

Do not place a bearer token or API key in this repository, JavaScript, query string, or local storage.

## 3. HHS ChatGPT handoff

This mode copies the user's pasted notebook/chart context plus question and opens `https://chatgpt.com/` in another tab. An authorized CDC/HHS user can sign in and select the organization-managed workspace there. This is a handoff, not an embedded or impersonated HHS login.

## Why not call the OpenAI API directly from GitHub Pages?

A static web page cannot safely keep a secret. OpenAI's API-key guidance says API keys must not be deployed in client-side environments such as browsers. In addition, ChatGPT Enterprise workspace membership and API Platform organization membership are managed separately, so an employee's ChatGPT workspace seat does not by itself provide programmatic API access.

For a production HHS integration, use an HHS-approved server-side gateway or other formally approved integration that handles identity, authorization, audit logging, data handling, and API credentials outside the browser.
