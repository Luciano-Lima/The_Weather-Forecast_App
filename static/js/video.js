class WeatherApp {
	constructor() {
		this.videoEl = document.querySelector('#video_Background video')
		this.sourceEl = this.videoEl.querySelector('source')
		this.forescast_descriptionEl = document.getElementById('forescast_description')
		this.bg_color = document.getElementById('bg_color')
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
