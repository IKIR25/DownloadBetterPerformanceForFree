from _hw_base import run

run(
    hw_type="storage",
    tier=1,
    name="8 TB SSD 2.0",
    spec="8 TB NVMe 2.0 • 5 PB/s Read • 0 ms Latency",
    full_name="8 TB Ultra SSD 2.0",
    color="#aa44ff",
    steps=[
        "Contacting storage servers...",
        "Formatting 8 TB...",
        "Creating NVMe file system...",
        "Calibrating NAND cells...",
        "Installing NVMe 2.0 drivers...",
        "Running speed check (5 PB/s)...",
        "Optimizing wear leveling...",
        "Complete!",
    ],
)
