import { useState, useEffect, useRef } from "react"

import styles from "./progressBar.module.css"

function ProgressBar(props) {
	const { progressChange, min, max } = props

	const [progress, setProgress] = useState(0)
	const [played, setPlayed] = useState(false)

	const scale = useRef([])
	// console.log(scale[progress])

	useEffect(() => {
		if (scale.current.length > 0) return

		const [minYear, minMonth] = min.split("-")
		const [maxYear, maxMonth] = max.split("-")

		let curMonth = +minMonth,
			curYear = +minYear

		while (curYear <= +maxYear) {
			scale.current.push(`${curYear}-${curMonth}`)
			if (curYear === +maxYear && curMonth === +maxMonth) break
			if (curMonth === 12) {
				curMonth = 0
				curYear += 1
			}
			curMonth += 1
		}
	}, [min, max, scale])

	useEffect(() => {
		if (!played) return
		const timer = setTimeout(() => {
			setProgress(prev => {
				if (progress === scale.current.length - 1) {
					setPlayed(false)
					return scale.current.length - 1
				}
				progressChange(scale.current[prev + 1])
				return prev + 1
			})
		}, 300)

		return () => {
			clearTimeout(timer)
		}
	}, [played, progress, progressChange, scale])

	const onClickHander = () => {
		setPlayed(prev => !prev)
	}

	const resetHandler = () => {
		progressChange("")
		setPlayed(false)
		setProgress(0)
	}

	return (
		<div className={styles.progressBarRoot}>
			<div className={styles.container}>
				<div className={styles.progressBar}>
					<div
						className={styles.progressBarFill}
						style={{
							width: `${
								progress > 0
									? (100 * (progress + 1)) /
									  scale.current.length
									: 0
							}%`,
						}}
					></div>
				</div>
				<div
					style={{ display: "flex", justifyContent: "space-between" }}
				>
					<label className="swap swap-rotate">
						<input type="checkbox" onClick={onClickHander} />

						<svg
							className="swap-on fill-current w-8 h-8"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
						>
							<path
								fillRule="evenodd"
								d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z"
								clipRule="evenodd"
							/>
						</svg>

						<svg
							className="swap-off fill-current w-8 h-8"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
						>
							<path
								fillRule="evenodd"
								d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm14.024-.983a1.125 1.125 0 010 1.966l-5.603 3.113A1.125 1.125 0 019 15.113V8.887c0-.857.921-1.4 1.671-.983l5.603 3.113z"
								clipRule="evenodd"
							/>
						</svg>
					</label>

					<div
						className={styles.progressLabel}
						style={{ marginLeft: `${0}%` }}
					>
						{!progress ? "Time Rolling!" : scale.current[progress]}
					</div>

					<label className="swap swap-rotate">
						<input type="checkbox" onClick={resetHandler} />

						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
							fill="currentColor"
							className="w-8 h-8"
						>
							<path d="M9.195 18.44c1.25.713 2.805-.19 2.805-1.629v-2.34l6.945 3.968c1.25.714 2.805-.188 2.805-1.628V8.688c0-1.44-1.555-2.342-2.805-1.628L12 11.03v-2.34c0-1.44-1.555-2.343-2.805-1.629l-7.108 4.062c-1.26.72-1.26 2.536 0 3.256l7.108 4.061z" />
						</svg>
					</label>
				</div>
			</div>
		</div>
	)
}

export default ProgressBar
