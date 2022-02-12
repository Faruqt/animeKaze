import { useState } from 'react';
import { useNavigate } from 'react-router';
import axios from "axios";

function Register(props) {
    const [error, setError] = useState(null)

    let navigate = useNavigate();

    const errorDiv = error 
      ? <div className="error">
          {error}
        </div> 
      : '';

    const [registerForm, setRegisterForm] = useState({
      username:"",
      email: "",
      password: ""
    })

    function registerMe(event) {
      axios({
        method: "POST",
        url:"/api/createuser",
        data:{
          username:registerForm.username,
          email: registerForm.email,
          password: registerForm.password
         }
      })
      .then((response) => {
          setRegisterForm(({
            username:"",
            email: "",
            password: ""
          }))
          setError(null)
          navigate('/login')
      }).catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
          setError(error.response.data.message)
          }
      })  
      event.preventDefault()
    }
    
    function handleChange(event) { 
      const {value, name} = event.target
      setRegisterForm(prevNote => ({
          ...prevNote, [name]: value})
      )}

    return (
      <div>
        <h1>Register</h1>
          <form className="register">
            <input onChange={handleChange} 
                  type="text"
                  text={registerForm.username} 
                  name="username" 
                  placeholder="Username" 
                  value={registerForm.username} />
            <input onChange={handleChange} 
                  type="email"
                  text={registerForm.email} 
                  name="email" 
                  placeholder="Email Address" 
                  value={registerForm.email} />
            <input onChange={handleChange} 
                  type="password"
                  text={registerForm.password} 
                  name="password" 
                  placeholder="Password" 
                  value={registerForm.password} />
            {errorDiv}
          <button onClick={registerMe}>Register</button>
        </form>
      </div>
    );
}

export default Register;
