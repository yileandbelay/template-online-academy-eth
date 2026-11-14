"""Capabilities the kernel itself provides. A block may require these without any block providing them (spec 5)."""

KERNEL_CAPABILITIES: tuple[str, ...] = (
    "TenancyV1",
    "AuthzV1",
    "AuditV1",
    "SettingsV1",
    "NumberingV1",
    "DocumentsV1",
    "LocalizationV1",
    "CalendarV1",
    "EventsV1",
    "JobsV1",
    "FilesV1",
    "SearchV1",
)
