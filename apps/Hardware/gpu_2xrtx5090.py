from _hw_base import run

run(
    hw_type="gpu",
    tier=2,
    name="2\u00d7 RTX 5090",
    spec="49152 CUDA Cores • 96 GB GDDR7 • NVLink • 2016 GB/s",
    full_name="2\u00d7 NVIDIA GeForce RTX 5090 NVLink",
    color="#00ddff",
    steps=[
        "Contacting NVIDIA servers...",
        "Materializing 49152 CUDA cores...",
        "Setting up NVLink bridge...",
        "Loading dual-GPU shaders...",
        "Calibrating 2\u00d7 ray tracing units...",
        "Installing dual-GPU drivers...",
        "Optimizing for 32K gaming...",
        "Complete!",
    ],
)
