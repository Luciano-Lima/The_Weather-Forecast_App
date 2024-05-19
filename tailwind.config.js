/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./templates/*html'],
	theme: {
		extend: {
			extend: {
				backgroundImage: {
					'hero-pattern': "url('../static/img/bg.jpeg')",
				},
			},
		},
	},
	plugins: [],
}
