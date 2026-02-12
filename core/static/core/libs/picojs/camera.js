let picoStream = null;
let rafId = null;

async function startCamera(video) {
	if (picoStream) return;

	picoStream = await navigator.mediaDevices.getUserMedia({
		video: { facingMode: "user" },
		audio: false,
	});

	video.srcObject = picoStream;
	await video.play();
}

function stopCamera(video) {
	if (!picoStream) return;

	picoStream.getTracks().forEach((t) => t.stop());
	picoStream = null;
	video.srcObject = null;
}

function startLoop(video, processfn) {
	let last = performance.now();

	function loop(now) {
		const dt = now - last;
		last = now;

		processfn(video, dt);
		rafId = requestAnimationFrame(loop);
	}

	rafId = requestAnimationFrame(loop);
}

function stopLoop() {
	cancelAnimationFrame(rafId);
	rafId = null;
}

function captureFrame(video) {
	const canvas = document.createElement("canvas");
	canvas.width = video.videoWidth;
	canvas.height = video.videoHeight;

	const ctx = canvas.getContext("2d");
	ctx.drawImage(video, 0, 0);

	return canvas;
}

function canvasToBlob(canvas) {
	return new Promise((resolve) => {
		canvas.toBlob((blob) => resolve(blob), "image/jpeg", 0.9);
	});
}
