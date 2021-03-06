import React, {useState, useEffect, useContext} from "react";
import { UserContext } from '../contexts/userContext';
import axios from "axios";
import InputEmoji from "react-input-emoji";
import { ReactComponent as Close } from '../../images/svg/closeButton.svg'

import photo from '../../images/photoIcon.png'
import emoji from '../../images/emoji.png'

function CreatePost(props){

	const [content, setContent] = useState("")
	const [image, setImage] = useState("");
	const [textArea, setTextArea] = useState(false)
	const avatar = window.localStorage.getItem('avatar')
	const userId = JSON.parse(window.localStorage.getItem("cuid"))
	const {token, removeToken}= useContext(UserContext)

	function expandTextArea(){
		setTextArea(true)
	}
	
	function onChangeFile(event){
		(
			(event.target.files && (event.target.files[0] != null)) &&
			setImage(URL.createObjectURL(event.target.files[0]))
		)
	}

	function cancelPost(){
		setImage(null)
		setTextArea(false)
	}

	function cancelImage(){
		setImage(null)
	}


	function submitForm (event){
		const formData = new FormData(event.target)
		formData.append("content", content);
		// console.log(formData.get(content))
		axios({
			method: "POST",
			url: '/api/upload',
			data:formData,
			headers: {
						Authorization: 'Bearer ' + token
			  		}
			}).then((response)=>{
				props.post() // get posts upon successful post submission
			}).catch((error) => {
				if (error.response) {
				  console.log(error.response)
				  if (error.response.status === 401){
					removeToken()
					}
				  }
			  	})
		setContent("")
		setTextArea(false)
		setImage(null)
		event.target.reset()
		event.preventDefault()
	}

	return (
		<div className="create-post">
			{textArea && <div className="post-top">
					<p>Create a post</p>
					<Close onClick={cancelPost}/>
				</div>
			}
			<form onSubmit={submitForm} encType="multipart/form-data" className="post-form">
				<div className="form-top">
					<div className='profile-image'>
						<img src={avatar} alt="profile logo"/>
					</div>
					{textArea ? <InputEmoji
						className='text'
						onChange={setContent}
						placeholder="What's happening?"
						value={content && content}
						required
					/>
					:
					<input onClick={expandTextArea} className='text' placeholder="What's happening?" type="text" required/>
					}
					
				</div>

				{image && <div className="picture-preview">
								<img className="preview" src={image} alt="preview" />
								<div>
									<Close onClick={cancelImage}/>
								</div>
						  </div>}
				<div className="form-bottom">
					<label onClick={expandTextArea} htmlFor="image"> <img src={photo} alt=""/> <p>Photo/Video</p>  </label>
					{!textArea ? <div className="emoji" onClick={expandTextArea}>  <img src={emoji} alt=""/> <p>Feeling</p> </div> : null}
					<input type="file" id="image" name="file" accept="image/*" className="file-custom" onChange={onChangeFile}/>
					<input  name="uid" value={userId} hidden readOnly={true}/>
					<button 
						className="sub-btn btn-lg btn-primary pull-xs-right"
						type="submit">
						Post
					</button>
				</div>
			</form>
		</div>
	)
}

export default CreatePost;
