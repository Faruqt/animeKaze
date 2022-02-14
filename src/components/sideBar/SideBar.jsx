import { useContext } from 'react'
import { UserContext } from '../contexts/userContext'
import CreateButton from './sideButtons'

function Sidebar(props) {
  const {token}= useContext(UserContext);
  const avatar = window.localStorage.getItem('avatar')
  const username = window.localStorage.getItem('username')
  const { unAuthButtons, AuthButtons, isActive , iconColor} = CreateButton();
  

  console.log(iconColor)
  return (
    <>
    <div className="side-bar">
      <div className="bar-content">
        {(!token && token !== "" && token !== undefined) ? 
          <>
          {unAuthButtons.map(item => <div key={item.id}>
                                <button  onClick={item.action}> 
                                        <item.icon className="icons" stroke={iconColor}/> 
                                        <p className="side-text">{item.text}</p>
                                </button> 
                              </div> 
                              )}
          <button className="bar-contents">
              <p>hello</p>
          </button>
          </>
        :
          <>

          {AuthButtons.map(item => <div key={item.id}>
                                <button className={isActive === item.id ? 'active-button' : ''} 
                                          onClick={() => item.action(item.id)}> 
                                        <item.icon className="icons" stroke= {isActive === item.id ? iconColor : '#546E7A'}/> 
                                        <p className="side-text">{item.text}</p>
                                </button> 
                              </div> 
                              )}
            <div className="myProfile">
              <div className='profileImage'>
                <img src={avatar} alt="profile logo"/>
              </div>
              <p>{username}</p>
            </div>
          </>
        }
      </div>
    </div>
    </>
  );
}

export default Sidebar;