def icon_html(name: str, size: int = 18, color: str = "#0f172a") -> str:
    """Return inline SVG markup for a named UI icon."""
    icons = {
        "lock": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M12 17a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm6-7h-1V8a5 5 0 0 0-10 0v2H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2zm-8-2a3 3 0 0 1 6 0v2h-6V8z' /></svg>",
        "mail": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z' /></svg>",
        "shield": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M12 2 4 5v6c0 5.05 3.39 9.82 8 10 4.61-.18 8-4.95 8-10V5l-8-3z' /></svg>",
        "graduation_cap": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M12 3 1 7l11 4 9-4-9-4zm0 5.09 7.18 3.61L12 15.08 4.82 11.7 12 8.09zM12 13.84 4 10.57v4.95l8 4 8-4v-4.95l-8 3.27z' /></svg>",
        "calendar": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M19 4h-1V2h-2v2H8V2H6v2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11zm0-13H5V6h14v1z' /></svg>",
        "school": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M12 3 1 7l11 4 9-4-9-4zm-1 13.07V15h2v1.07c1.66.42 3 1.92 3 3.43v2.5h-2v-2.5c0-.83-.67-1.5-1.5-1.5h-1c-.83 0-1.5.67-1.5 1.5v2.5H8v-2.5c0-1.51 1.34-3.01 3-3.43z' /></svg>",
        "professor": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor'><path d='M12 2 1 6l11 4 9-4-8-4zM6 18c0-3.31 2.69-6 6-6s6 2.69 6 6v2H6v-2zm6-4a4 4 0 0 0-4 4v.5h8V18a4 4 0 0 0-4-4z' /></svg>"
    }
    svg = icons.get(name, "")
    if not svg:
        return ""
    return (
        f"<span style='display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;" \
        f"vertical-align:text-bottom;color:{color};margin-right:0.35rem;'>{svg}</span>"
    )

PAGE_ICON_URI = (
    "data:image/svg+xml;charset=utf-8," \
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E" \
    "%3Cpath fill='currentColor' d='M12 3 1 7l11 4 9-4-9-4zm-5 8.07V11h10v.07L12 14.32 7 11.07zM5 12.57 12 16.92l7-4.35V18H5v-5.43z'/%3E" \
    "%3C/svg%3E"
)
