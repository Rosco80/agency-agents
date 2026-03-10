# Italian Logistics AI Campaign: Lead Automation Setup

This document outlines the exact workflow required to handle inbound leads automatically after they submit the Formspree form on `logistics.autoflow-solutions.com`.

**Objective:** Instantly nurture the lead, log their data for sales, and notify our team without manual intervention.

## The Automation Stack Fast-Track

We recommend using **Make (formerly Integromat)** or **Zapier** for this, as both integrate natively with Formspree and offer free tiers that are more than sufficient for campaign launches.

### The Trigger
*   **App:** Formspree
*   **Event:** "New Submission"
*   **Form:** Select the Italian Logistics AI form.

---

## Action 1: The Automated Welcome Email
When a fleet manager requests an audit, speed is critical. They need immediate confirmation.

*   **App:** Gmail / Outlook / Instantly
*   **Event:** "Send Email"
*   **To:** `{{Email Aziendale}}` (from Formspree)
*   **From:** Your Autoflow address.

**Email Template (Italian):**

**Subject:** Abbiamo ricevuto la tua richiesta per l'Audit della Flotta

**Body:**
> Ciao `{{Nome}}`,
>
> Grazie per l'interesse verso Autoflow Solutions. Ho ricevuto la tua richiesta per un Audit 1:1 della tua flotta da `{{Dimensione Flotta}}` camion.
>
> Per far sì che l'audit sia il più preciso possibile, ho solo un paio di brevi domande preparatorie prima di fissare la nostra chiamata:
> 
> 1. Qual è la percentuale approssimativa di tratte urbane (centro città/ZTL) rispetto alle tratte autostradali?
> 2. Quale software o metodo usate attualmente per assegnare i carichi giornalieri?
>
> Rispondi pure a questa email quando hai un attimo. Successivamente, ti invierò un link per scegliere l'orario migliore per la nostra analisi su Zoom.
>
> A presto,
> 
> [Tuo Nome]
> Autoflow Solutions

---

## Action 2: CRM Logging (Optional but Recommended)
Instead of letting leads sit in your email inbox, push them into a CRM so you can track who you've followed up with.

*   **App:** HubSpot (Free CRM), Pipedrive, or Google Sheets
*   **Event:** "Create Contact" / "Add Row"
*   **Data Mapping:**
    *   Name -> `{{Nome}}`
    *   Email -> `{{Email Aziendale}}`
    *   Fleet Size -> `{{Dimensione Flotta}}`
    *   Lead Source -> "Campaign: Italian Logistics LP"
    *   Status -> "New Lead"

---

## Action 3: Internal Notification
The moment a lead comes in, you want to know.

*   **App:** Slack or WhatsApp (via Twilio/click-to-chat)
*   **Event:** "Send Channel Message"
*   **Channel:** `#sales-leads`
*   **Message:**
    > 🚨 **Nuovo Audit Richiesto!**
    > **Nome:** `{{Nome}}`
    > **Email:** `{{Email Aziendale}}`
    > **Flotta:** `{{Dimensione Flotta}}` camion
    > *L'email di benvenuto è stata inviata automaticamente.*

## Next Steps to Implement
1. Log in to your Zapier or Make account.
2. Select Formspree as your trigger app and connect your account.
3. Add the Gmail module and paste the template above.
4. Turn on the automation. Test it by filling out the form on your live site!
