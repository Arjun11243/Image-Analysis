from google.cloud import documentai_v1 as documentai
import os

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """Processes a document and returns the extracted entities."""
    client = documentai.DocumentProcessorServiceClient()

    # Construct the fully qualified processor path
    parent = f"projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version}"
    document = documentai.RawDocument(content=open(file_path, "rb").read(), mime_type=mime_type)

    # Process the document
    request = documentai.ProcessRequest(name=parent, raw_document=document)
    result = client.process_document(request=request)

    return result.document


def print_entity(entity: documentai.Document.Entity) -> None:
    """Prints the details of an entity."""
    key = entity.type_
    text_value = entity.mention_text  # Use mention_text instead of text_anchor.content
    normalized_value = entity.normalized_value.text
    print(f"    * {repr(key)}: {repr(text_value)}")

    if normalized_value:
        print(f"    * Normalized Value: {repr(normalized_value)}")



def process_document_entity_extraction_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    output_file: str,
) -> None:
    """Processes a document, prints the extracted entities, and writes them to a file automatically."""
    document = process_document(project_id, location, processor_id, processor_version, file_path, mime_type)

    print(f"Found {len(document.entities)} entities:")
    with open(output_file, 'w') as file:
        for entity in document.entities:
            print_entity(entity)
            file.write(f"{entity.type_}: {entity.mention_text}\n")

# Example usage
# project_id = "529876974990"
# location = "us"
# processor_id = "35a86c53df6f4b1"  # Create processor before running sample
# processor_version = "f1dece949e79896f"  # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
# file_path = "vp3.jpg"
# mime_type = "image/jpeg"
# output_file = "entities.txt"

# process_document_entity_extraction_sample(project_id, location, processor_id, processor_version, file_path, mime_type, output_file)
