/**
 * Google Apps Script — Subscritores MarctechJA
 * 
 * Como usar:
 * 1. Cria uma Google Sheet em https://sheets.google.com
 * 2. Nomeia a primeira folha como "Subscritores"
 * 3. Vai a Extensões > Apps Script
 * 4. Cola este código e grava (Ctrl+S)
 * 5. Clica em "Implementar" > "Nova implementação" > "Aplicação Web"
 * 6. Executar como: "Eu" | Quem tem acesso: "Qualquer pessoa"
 * 7. Clica em "Implementar" e copia o URL da aplicação web
 * 8. Escreve esse URL em blog/index.html no form action
 *    (substituir a linha do form action)
 */

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Subscritores");

    // Ensure header row exists
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Data", "Nome", "WhatsApp", "Email", "Canal Preferido"]);
    }

    const params = e.parameter;
    const data = [
      new Date().toISOString(),
      params.nome || "",
      params.whatsapp || "",
      params.email || "",
      params.canal || ""
    ];

    sheet.appendRow(data);

    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok" }))
    .setMimeType(ContentService.MimeType.JSON);
}
