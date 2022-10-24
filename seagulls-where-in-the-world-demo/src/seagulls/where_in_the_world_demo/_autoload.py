"""
Random ideas:
- spawn a sub-process that is responsible for streaming images
- monitor the sub-process and handle interruptions
- parent process is the tiniest possible code to open a window and stream the images
- parent process pushes user input data to sub-process decoupled from game frames
- mouse rendering can be handled by parent process if we need to improve latency
- we can improve latency further by streaming game object positions and sprite information
- sprite information can include interaction rendering differences
"""
