/**
 * Google Apps Script — Subscritores MarctechJA
 *
 * COMO USAR:
 * 1. https://sheets.google.com — cria uma folha nova
 * 2. Nomeia a primeira folha (baixo) como "Subscritores"
 * 3. Extensões > Apps Script
 * 4. Cola este codigo, grava (CTRL+S)
 * 5. Implementar > Nova implementacao > Aplicacao Web
 *    Executar como: Eu   |   Quem tem acesso: Qualquer pessoa
 * 6. Clica "Implementar" — avanca se aparecer aviso
 * 7. Copia o URL (https://script.google.com/macros/s/.../exec)
 * 8. Diz-me o URL que eu atualizo o site
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Subscritores");
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["Data", "Nome", "WhatsApp", "Email", "Canal Preferido"]);
    }
    var params = e.parameter;
    sheet.appendRow([
      new Date().toISOString(),
      params.nome || "",
      params.whatsapp || "",
      params.email || "",
      params.canal || ""
    ]);
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
