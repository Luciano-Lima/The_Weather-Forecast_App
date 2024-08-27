class WeatherApp {
	constructor() {
		this.videoEl = document.querySelector('#video_Background video')
		this.sourceEl = this.videoEl.querySelector('source')
		this.forecast_descriptionEl = document.getElementById('forecast_description')
		this.bg_color = document.getElementById('bg_color')
	}

	updateVideoBackground() {
		let weatherDescription = this.forecast_descriptionEl
			? this.forecast_descriptionEl.innerText.trim().toLowerCase()
			: ''
		let videoSource

		// Ensure weather description is valid
		if (weatherDescription === '') {
			console.log('Weather description is not available.')
			return
		}

		switch (weatherDescription) {
			case 'clear sky':
				videoSource = '../static/video/clear_sky.mp4'
				this.bg_color.style.backgroundColor = '#426b9b85'
				break
			case 'scattered clouds':
				videoSource = '../static/video/scatted_clouds.mp4'
				this.bg_color.style.backgroundColor = '#4b647ba6'
				break
			case 'overcast clouds':
				videoSource = '../static/video/overcast_clouds.mp4'
				this.bg_color.style.backgroundColor = '#89898961'
				break
			case 'few clouds':
				videoSource = '../static/video/few_clouds.mp4'
				break
			case 'broken clouds':
				videoSource = '../static/video/broken_clouds.mp4'
				this.bg_color.style.backgroundColor = '#60606094'
				break
			case 'light rain':
				videoSource = '../static/video/light_rain.mp4'
				this.bg_color.style.backgroundColor = '#9e9ea282'
				break
			default:
				videoSource = '../static/video/video_background.mp4'
		}

		// Add cache-busting query string to prevent caching issues
		const uniqueVideoSource = `${videoSource}?t=${new Date().getTime()}`

		// Compare only the relative part of the source URL to avoid issues with base URL differences
		const currentSrc = this.sourceEl.src.split('?')[0] // remove cache-busting part if present

		//load and play video if the source has changed
		if (!currentSrc.includes(videoSource)) {
			this.sourceEl.src = uniqueVideoSource
			this.videoEl.load()

			this.videoEl.play().catch((err) => {
				// Handle video play errors, especially on mobile devices
				console.error('Video playback failed', err)
			})
		}
	}

	init() {
		// Initial call when the page loads
		this.updateVideoBackground()

		// Monitor for changes in the forecast description dynamically
		const observer = new MutationObserver(() => this.updateVideoBackground())
		if (this.forecast_descriptionEl) {
			observer.observe(this.forecast_descriptionEl, { childList: true, subtree: true })
		}
		// Listen for input changes on the city field to potentially trigger background updates
		const cityInput = document.getElementById('city')
		cityInput.addEventListener('input', () => {
			setTimeout(() => this.updateVideoBackground(), 500)
		})
	}
}

document.addEventListener('DOMContentLoaded', () => {
	const app = new WeatherApp()
	app.init()
})
