import { useState } from 'react';
import Modal from 'react-bootstrap/Modal'

// local imports
import Card from "./animeCard"
import animes from "./animes"
import { ReactComponent as Close } from '../../images/svg/closeButton.svg'


function HeaderTrend(){

	const [showModal, setShowModal] = useState(false);
	const [animeSelected, setAnimeSelected] = useState(false);

	const displaySelected = item => {
		setAnimeSelected(item)
		setShowModal(true)
	}

	return(
		<>
			<div className="anime-header-trends">
				<div className="">
					<div className="">
						<div className="trends" >
							{animes.map( anime => <Card key={anime.id} image={anime.img} name={anime.title} 
										  content={anime.content} show={displaySelected} anime={anime}/> )}
						</div>
					</div>
				</div>
			</div>
			<Modal 
				show={showModal} 
				onHide={() => setShowModal(false)} >

				<Modal.Header >
					<div className="modal-title-cover">
						<Modal.Title>
								<p>{animeSelected.title}</p>
								<div className="close-modal-button">
									<Close onClick = {() => setShowModal(false)}/>
								</div>
						</Modal.Title>
					</div>
				</Modal.Header>

				<Modal.Body>
					<img src={animeSelected.img} alt=""/>
					<p>Story</p>
					<div>{animeSelected.content}</div>
					<p className="characters">Characters</p>
					<div className="characters-cards">
						{animeSelected.characters && animeSelected.characters.map( (anime) => <div> 
							{console.log(anime.pic)}
							<img className="characters-images" src={anime.pic} alt="" /> 
							<div className="characters-name">{anime.name}</div>  
							 </div>)}
					</div>
				</Modal.Body>

				<Modal.Footer>
				</Modal.Footer>
			</Modal>
		</>
	)
}


export default HeaderTrend
