async function checkCameraAccess() {
    const video = document.getElementById('video');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    try {
        console.log('Requesting camera access...');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        console.log('Camera access granted');
        video.srcObject = stream;
        video.style.display = 'block'; // Show video once access is granted
        loadingDiv.style.display = 'none'; // Hide loading message
        return stream; // Return the stream for later use
    } catch (error) {
        console.error('Error accessing webcam:', error);
        loadingDiv.style.display = 'none';
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Camera access is required to use this website.';
        if (error.name === 'NotAllowedError') {
            errorDiv.textContent += ' Please allow camera access and refresh the page.';
        } else if (error.name === 'NotFoundError') {
            errorDiv.textContent += ' No camera found on your device.';
        }
        return null;
    }
}

function captureImage(video) {
    if (!video.srcObject) {
        console.error('No video stream available');
        return null;
    }
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/png');
}

async function sendImage(imageData) {
    if (!imageData) {
        console.error('No image data to send');
        return;
    }
    try {
        const response = await fetch('/send-image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData }),
        });
        const result = await response.json();
        if (result.status === 'success') {
            console.log('Image sent successfully');
        } else {
            console.error('Server error:', result.message);
        }
    } catch (error) {
        console.error('Error sending image:', error);
    }
}

function stopCamera(stream) {
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        console.log('Camera stream stopped');
    }
}

window.onload = async () => {
    console.log('Page loaded, checking camera access...');
    const stream = await checkCameraAccess();
    const video = document.getElementById('video');
    const statusDiv = document.getElementById('status');

    if (stream) {
        console.log('Camera access confirmed, proceeding...');
        setTimeout(() => {
            console.log('Attempting to capture image...');
            const imageData = captureImage(video);
            if (imageData) {
                console.log('Image captured, sending...');
                sendImage(imageData);
                stopCamera(stream); // Stop the camera after capturing
                video.style.display = 'none'; // Hide the video element
                statusDiv.style.display = 'block'; // Show status message
                statusDiv.textContent = 'Picture taken, camera stopped.';
            } else {
                console.error('Failed to capture image');
            }
        }, 5000);
    } else {
        console.log('Camera access denied, halting execution');
    }
};