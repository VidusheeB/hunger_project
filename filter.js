import styles from "./styles.module.css"

function Filter(props) {
	const { title, datas, id, stateChange, type } = props

	const onClickHandler = e => {
		stateChange(e.target.value)
	}

	if (type === "select")
		return (
			<div className={`form-control w-full max-w-xs ${styles.filter}`}>
				<label className='label'>
					<span className='label-text'>{title}</span>
				</label>
				<select
					className='select select-bordered'
					onChange={onClickHandler}
					defaultValue={"DEFAULT"}
				>
					<option disabled value='DEFAULT'>
						Pick one
					</option>
					{datas.map(data => (
						<option onClick={onClickHandler} key={`${id}-${data}`}>
							{data}
						</option>
					))}
				</select>
			</div>
		)

	if (type === "month")
		return (
			<div>
				<label className='label'>
					<span className='label-text'>{title}</span>
				</label>
				<input
					type='month'
					placeholder='Type here'
					className='input input-bordered w-full max-w-xs'
					defaultValue={"2021-12"}
					onChange={onClickHandler}
					min={datas.min}
					max={datas.max}
				/>
			</div>
		)
}

export default Filter
