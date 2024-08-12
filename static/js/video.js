class WeatherApp {
	constructor() {
		this.videoEl = document.querySelector('#video_Background video')
		this.sourceEl = this.videoEl.querySelector('source')
		this.forescast_descriptionEl = document.getElementById('forescast_description')

		console.log('Video Element:', this.videoEl)
		console.log('Source Element:', this.sourceEl)
		console.log('Forecast Description Element:', this.forescastDescriptionEl)
	}

	updateVideoBackground() {
		let weatherDescription = this.forescast_descriptionEl.innerText.trim().toLowerCase()
		let videoSource

		// Check if weatherDescription is not empty or undefined
		if (weatherDescription === '') {
			console.log('Weather description is not available.')
			return
		}

		switch (weatherDescription) {
			case 'clear sky':
				videoSource = '../static/video/storm.mp4'
				break
			case 'scattered clouds':
				videoSource = '../static/video/blue_Sky.mov'
				break
			default:
				videoSource = '../static/video/sunset.mp4'
		}
		// Force update the source element's src attribute
		const uniqueVideoSource = `${videoSource}?t=${new Date().getTime()}`
		this.sourceEl.src = uniqueVideoSource

		// Reload and play the video
		this.videoEl.load()
		this.videoEl.play()
	}

	init() {
		const cityInput = document.getElementById('city')
		cityInput.addEventListener('input', () => {
			setTimeout(() => this.updateVideoBackground(), 500)
		})

		// Initial call when the page loads
		this.updateVideoBackground()
	}
}

document.addEventListener('DOMContentLoaded', () => {
	const app = new WeatherApp()
	app.init()
})
