import React, {useState, useEffect, useContext} from "react";
import axios from "axios";
import { UserContext } from './contexts/userContext';
import Search from "./Search"

function Posts(props){
	return (
            <div className="note">
                <h1 >  {props.content} </h1>
				<img alt={""} src={props.image} />
            </div>
    )
}
function Home(){

	// const [postMessage, setpostMessage] = useState("")
    const [posts, setPosts] = useState("")
	const [content, setContent] = useState("")
    const {token, removeToken, setAppState}= useContext(UserContext);
	const username = window.localStorage.getItem('username')
	const userId = JSON.parse(window.localStorage.getItem("cuid"))

    useEffect(() => {
		// setAppState({ loading: true });
        getPosts()
		// console.log("here")
    },[])

	function handleChange(event) { 
		const post = event.target.value
		setContent(post)
	}

    function getPosts(){
		console.log(username)
		axios({
			method: "GET",
			url:'/api/'+ username + '/posts',
			headers: {
			  Authorization: 'Bearer ' + token
			}
		  }).then((response)=>{
			setPosts(
                response.data.items
			  )
			// setAppState({ loading: false });
		  }).catch((error) => {
			if (error.response) {
			  console.log(error.response);
			  console.log(error.response.status);
			  if (error.response.status === 401){
				  removeToken()
			  }
			  console.log(error.response.headers);
			  }
		  })}

	function submitForm (event){
		const formData = new FormData(event.target)
		axios({
			method: "POST",
			url: '/api/upload',
			data:formData
			}).then((response)=>{
				getPosts() // get posts upon successful post submission
			  }).catch((error) => {
				if (error.response) {
				  console.log(error.response)
				  }
			  })
		setContent("")
		event.target.reset()
		event.preventDefault()
		}
		
    return (
        <>
            <Search />
			<form onSubmit={submitForm} encType="multipart/form-data" className="create-note">
				<input  type="text" onChange={handleChange} name="content" placeholder="What's happening?" value={content} required/>
				<input type="file" id="image" name="file" accept="image/*" className="file-custom" required/>
				<input  name="uid" value={userId} hidden readOnly={true}/>
				<button
					className="btn btn-lg btn-primary pull-xs-right"
					type="submit">
					Post
				</button>
			</form>
            <div className="note">
                <h1 >  Welcome to AnimeKaze </h1>
            </div>
			{posts && posts.map(posts => <Posts key={posts.id} content={posts.content} image={posts.image}/>)}
        </>
    )
}

export default Home;
