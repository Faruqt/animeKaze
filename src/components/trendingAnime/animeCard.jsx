
function Card(props){
	return(
		<div className="anime" onClick={ () => props.show(props.anime) } > 
			<div className="cover">
				<img src={props.image} alt=""/>
			</div>
			<div className="content">
				<p>{props.name}</p>
				<p>{props.content}</p>
			</div>
		</div>
	)
}


export default Card
