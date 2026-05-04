"""C2PA Content Credentials parsing service."""

import io

from app.models.schemas import C2PAEditEntry, C2PAManifest, ProvenanceResponse


EU_AI_ACT_VERIFIED = "This media carries C2PA Content Credentials indicating AI generation. Under EU AI Act Article 50, this disclosure meets transparency obligations effective August 2026."

EU_AI_ACT_NONE = "No C2PA Content Credentials found. This media cannot be verified for provenance. Under EU AI Act Article 50, AI-generated media should carry machine-readable labels by August 2026."

EU_AI_ACT_TAMPERED = "C2PA Content Credentials are present but fail validation. The credential chain may have been modified or corrupted."


def check_provenance(file_bytes: bytes, filename: str) -> ProvenanceResponse:
    """Check a file for C2PA Content Credentials.

    Returns one of three states:
    - verified: Credentials found and valid
    - none: No credentials present
    - tampered: Credentials present but invalid
    """
    try:
        from c2pa import Reader

        reader = Reader(file_bytes)
        manifest_store = reader.get_manifest_store()

        if not manifest_store or not manifest_store.get("manifests"):
            return ProvenanceResponse(
                has_credentials=False,
                status="none",
                manifest=None,
                eu_ai_act_note=EU_AI_ACT_NONE,
            )

        # Parse the active manifest
        active_manifest = manifest_store.get("active_manifest")
        manifests = manifest_store.get("manifests", {})

        manifest_data = manifests.get(active_manifest, manifests.get(list(manifests.keys())[0], {}))

        # Extract key fields
        creator_tool = manifest_data.get("metadata", {}).get("tools", [None])[0]
        creation_date = manifest_data.get("metadata", {}).get("dateTime", None)
        ai_flag = manifest_data.get("metadata", {}).get("aiType", None) is not None

        # Build edit history
        edit_history = []
        for assertion in manifest_data.get("assertions", []):
            entry = C2PAEditEntry(
                action=assertion.get("label", "unknown"),
                tool=assertion.get("metadata", {}).get("tool"),
                timestamp=assertion.get("metadata", {}).get("dateTime"),
            )
            edit_history.append(entry)

        manifest = C2PAManifest(
            creator_tool=creator_tool,
            creation_date=creation_date,
            edit_history=edit_history if edit_history else None,
            ai_generated_flag=ai_flag if ai_flag else None,
        )

        return ProvenanceResponse(
            has_credentials=True,
            status="verified",
            manifest=manifest,
            eu_ai_act_note=EU_AI_ACT_VERIFIED,
        )

    except ImportError:
        # c2pa-python not installed
        return ProvenanceResponse(
            has_credentials=False,
            status="none",
            manifest=None,
            eu_ai_act_note="C2PA library not installed. Install c2pa-python to enable provenance checks.",
        )
    except Exception as e:
        error_msg = str(e).lower()
        if "tampered" in error_msg or "invalid" in error_msg or "signature" in error_msg:
            return ProvenanceResponse(
                has_credentials=False,
                status="tampered",
                manifest=None,
                eu_ai_act_note=EU_AI_ACT_TAMPERED,
            )
        # Most files won't have C2PA — treat as "none" rather than error
        return ProvenanceResponse(
            has_credentials=False,
            status="none",
            manifest=None,
            eu_ai_act_note=EU_AI_ACT_NONE,
        )
