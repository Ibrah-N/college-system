async function deleteDoc(
  id
) {
  const confirmed = confirm("Are you sure you want to delete this document record?");
  if (!confirmed) return;

  const response = await fetch(`/docs/delete_doc/${id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    alert("Document record deleted successfully");
    window.location.reload();
  } else {
    const err = await response.json();
    alert(`Error: ${err.message || "Failed to delete document record"}`);
  }
}



async function exportDocs() {
  const form = document.querySelector("form");
  const formData = new FormData(form); // collects all inputs & selects

  const response = await fetch("/docs/export_docs", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    alert("Export failed");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "doc_table.csv"; // or .csv
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
