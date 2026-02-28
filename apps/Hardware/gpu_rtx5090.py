from _hw_base import run

run(
    hw_type="gpu",
    tier=1,
    name="RTX 5090",
    spec="24576 CUDA Cores • 48 GB GDDR7 • 1008 GB/s",
    full_name="NVIDIA GeForce RTX 5090",
    color="#00aaff",
    steps=[
        "Contacting NVIDIA servers...",
        "Materializing 24576 CUDA cores...",
        "Loading RTX shaders...",
        "Calibrating ray tracing units...",
        "Installing GPU drivers...",
        "Running 3DMark check...",
        "Optimizing for 8K gaming...",
        "Complete!",
    ],
)
