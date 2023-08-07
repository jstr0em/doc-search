function deleteDocument(docId) {
  fetch("/delete-document", {
    method: "POST",
    body: JSON.stringify({ docId: docId }),
  }).then((_res) => {
    window.location.href = "/documents";
  });
}
