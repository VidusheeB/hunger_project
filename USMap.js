import { useState, useEffect } from "react"
import ProgressBar from "./progressBar"
import * as d3 from "d3"
import * as topojson from "topojson"
import Filter from "./filter"
import ca_data from "../data/CA.json"
import tx_data from "../data/TX.json"
import SNAP_data from "../data/2019-2023_dashboard.json"
import SNAP_data from "../data/SNAP_20192022.json"

import styles from "./styles.module.css"

function USMap() {
	const [selectState, setSelectState] = useState("Select State")
	const [selectDate, setSelectDate] = useState({ year: 2021, month: 12 })
	const [progress, setProgress] = useState("")

	const stateChangeHandler = value => {
		if (value.includes("-")) {
			const [year, month] = value.split("-")
			setSelectDate({ year: +year, month: +month })
		} else {
			setSelectState(value)
		}
	}

	const progressChangeHandler = curProgress => {
		setProgress(curProgress)
	}

	useEffect(() => {
		async function render() {
			let renderData
			if (
				selectState === "Select State" ||
				selectState === "United States"
			) {
				const mapData = await fetch(
					"https://raw.githubusercontent.com/no-stack-dub-sack/testable-projects-fcc/master/src/data/choropleth_map/counties.json",
				).then(res => res.json())

				renderData = topojson.feature(
					mapData,
					mapData.objects.counties,
				).features
			}

			if (selectState === "California") {
				renderData = topojson.feature(
					ca_data,
					ca_data.objects.cb_2015_california_county_20m,
				).features
			}

			if (selectState === "Texas") {
				renderData = topojson.feature(
					tx_data,
					tx_data.objects.cb_2015_texas_county_20m,
				).features
			}

			let filter_SNAP_data

			if (progress === "") {
				filter_SNAP_data = SNAP_data.filter(
					data =>
						data.Year === selectDate.year &&
						data.Month === selectDate.month,
				)
			}

			if (progress !== "") {
				const [curYear, curMonth] = progress.split("-")
				filter_SNAP_data = SNAP_data.filter(
					data => data.Year === +curYear && data.Month === +curMonth,
				)
			}

			// console.log(filter_SNAP_data)

			// console.log(SNAP_data)

			// console.log(renderData)

			// if (progress !== "") {

			// }

			// if (selectYear !== "Select Year") {
			// 	eduData.forEach(edu => {
			// 		edu.bachelorsOrHigher = (
			// 			edu.bachelorsOrHigher *
			// 			(+selectYear - 2017)
			// 		).toFixed(2)
			// 	})
			// }

			const w = 1200
			const h = 600
			// const padding = 70

			// clear svg
			const chart = document.getElementById("theChart")
			if (chart) {
				chart.innerHTML = ""
			}

			const svg = d3
				.select("#theChart")
				.append("svg")
				.attr("width", w)
				.attr("height", h)
				.attr("align-self", "center")
			// .attr("transform", "scale(1, -1)")

			svg.selectAll("path")
				.data(renderData)
				.enter()
				.append("path")
				.attr("d", d3.geoPath())
				.attr("class", d => {
					// console.log(d)
					// return handleGetBachelors(d)
					return handleSNAPData(d)
				})
				// .attr("stroke", "#ddd")
				// .attr("stroke-width", "0.2px")
				.on("mouseover", handleMouseOver)
				.on("mouseout", handleMouseOut)

			function handleSNAPData(d) {
				for (let i = 0; i < filter_SNAP_data.length; i++) {
					if (
						d.id === +filter_SNAP_data[i].fipsValue ||
						+d?.properties.GEOID === +filter_SNAP_data[i].fipsValue
					) {
						return filter_SNAP_data[i].Flag
					}
				}
				return "Grey"
			}

			// function handleGetBachelors(d) {
			// 	for (let i = 0; i < eduData.length; i++) {
			// 		if (
			// 			d.id === eduData[i].fips ||
			// 			eduData[i].area_name.startsWith(d?.properties.NAME)
			// 		) {
			// 			return handleGetColor(eduData[i].bachelorsOrHigher)
			// 		}
			// 	}
			// }

			// function handleGetColor(x) {
			// 	if (x <= 12) {
			// 		return "color-01"
			// 	} else if (x > 12 && x <= 21) {
			// 		return "color-02"
			// 	} else if (x > 21 && x <= 30) {
			// 		return "color-03"
			// 	} else if (x > 30 && x <= 39) {
			// 		return "color-04"
			// 	} else if (x > 39 && x <= 48) {
			// 		return "color-05"
			// 	} else if (x > 48 && x <= 57) {
			// 		return "color-06"
			// 	} else if (x > 57) {
			// 		return "color-07"
			// 	} else {
			// 		return "color-error"
			// 	}
			// }

			var tooltip = d3
				.select("#theChart")
				.append("div")
				.style("position", "absolute")
				.style("visibility", "hidden")
				.style("background-color", "#edf8c2")
				.style("color", "black")
				.style("border", "solid")
				.style("border-width", "0px")
				.style("border-radius", "15px")
				.style("padding", "10px")
				.style("box-shadow", "2px 2px 20px")
				.style("opacity", "0.85")
				.attr("id", "tooltip")

			function handleMouseOver(event, d) {
				d3.select(this).attr("stroke", "black")
				tooltip
					.style("visibility", "visible")
					.style("top", event.pageY - 40 + "px")
					.style("left", event.pageX + 10 + "px")
					.html(
						"<center> " +
							handleGetLocation(d.id || +d.properties.GEOID) +
							" </center>",
					)
			}

			function handleGetLocation(x) {
				console.log(x)
				// for (let i = 0; i < eduData.length; i++) {
				// 	if (
				// 		x === eduData[i].fips ||
				// 		eduData[i].area_name.startsWith(x)
				// 	) {
				// 		return (
				// 			eduData[i].area_name +
				// 			", " +
				// 			eduData[i].state +
				// 			": " +
				// 			eduData[i].bachelorsOrHigher +
				// 			"%"
				// 		)
				// 	}
				// }

				const node = filter_SNAP_data.find(
					data => +data.fipsValue === x,
				)

				console.log(node)

				if (!node) return "No Data Available"
				return `${node.County.substring(0, node.County.length - 7)}, ${
					node.State === "California" ? "CA" : "TX"
				}<br>${
					node.Year < 2022 ? "Applications" : "Predict Applications"
				}: ${node.SNAP_Applications || Math.floor(node.pred_snap)}
				 <br>Population Density: ${node.PDensity}
				 <br>Population: ${node.Population} <br>
				 ${node.Predicted === 1 ? "Predicted: true" : ""}
				 `
			}

			// <br>worker: ${node.last_worker}
			// <br>disaster: ${node.last_disaster}

			function handleMouseOut(event, d) {
				d3.select(this).attr("stroke", "none")
				tooltip.style("visibility", "hidden")
			}

			// Begin legend stuff

			// const legW = w / 5
			// const legH = 20
			// const legendColors = [12, 21, 30, 39, 48, 57, 66]
			const texts = [
				{ text: "High Risk", color: "Red" },
				{ text: "Elevated Risk", color: "YellowTitle" },
				{ text: "Stable Risk", color: "GreenTitle" },
				{ text: "No data available", color: "GreyTitle" },
			]

			let legend = svg
				.append("g")
				.attr("transform", "translate(800, 300)")
				.attr("id", "legend")

			legend
				.selectAll("mydots")
				.data(texts.map(each => each.text))
				.enter()
				.append("circle")
				.attr("cx", 100)
				.attr("cy", function (d, i) {
					return 100 + i * 25
				}) // 100 is where the first dot appears. 25 is the distance between dots
				.attr("r", 7)
				.attr("class", (d, i) => texts[i].color)

			legend
				.selectAll("mylabels")
				.data(texts.map(each => each.text))
				.enter()
				.append("text")
				.attr("x", 120)
				.attr("y", function (d, i) {
					return 100 + i * 25
				}) // 100 is where the first dot appears. 25 is the distance between dots
				.attr("class", (d, i) => texts[i].color)
				.text(d => d)
				.attr("text-anchor", "left")
				.style("alignment-baseline", "middle")
				.style("font-size", "16px")

			// console.log(legend)

			// let xScale = d3.scaleLinear().domain([0, 70]).range([0, legW])

			// let xAxis = d3
			// 	.axisBottom()
			// 	.scale(xScale)
			// 	.ticks(7)
			// 	.tickSize(30)
			// 	.tickFormat(
			// 		(d, i) =>
			// 			["3%", "12%", "21%", "30%", "39%", "48%", "57%", "66%"][
			// 				i
			// 			],
			// 	)

			// legend
			// 	.selectAll("rect")
			// 	.data(legendColors)
			// 	.enter()
			// 	.append("rect")
			// 	.attr("width", legW / legendColors.length)
			// 	.attr("height", legH)
			// 	.attr("x", (d, i) => i * (legW / legendColors.length))
			// 	.attr("class", d => handleGetColor(d))

			// legend.append("g").call(xAxis)
		}
		render()
	}, [selectState, selectDate, progress])

	return (
		<div id="container">
			<h1 id="title">United States Food Assistance Dashboard</h1>
			<div id="description">
				SNAP food assistance application collected by Google Trends
				(2019-2023)
			</div>
			<div style={{ display: "flex", justifyContent: "space-between" }}>
				<ProgressBar
					progressChange={progressChangeHandler}
					min={"2019-02"}
					max={"2021-12"}
				/>

				<div className={styles.filterRoot}>
					<Filter
						title={"Pick a Month"}
						datas={{ min: "2019-02", max: "2021-12" }}
						id="month"
						stateChange={stateChangeHandler}
						className={styles.filter}
						type="month"
					/>

					<Filter
						title={"Select State"}
						datas={["United States", "California", "Texas"]}
						id="state"
						stateChange={stateChangeHandler}
						className={styles.filter}
						type="select"
					/>
				</div>
			</div>

			<div id="theChart"></div>
			<div id="theLegend"></div>
		</div>
	)
}

export default USMap
