import { useState } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom'
import { UserContext } from '../contexts/userContext';

//Application
import Home from "../Homepage"
import Explore from "../explore/Explore"
import Base from "../Basepage"
import Trend from "../trendingAnime/trending"
import Header from "../Header/Header"
import Settings from "../settings/settings"
import Sidebar from "../sideBar/SideBar"

// import CurrentUser from "./getUser"

// Auth
import AuthedRoute from '../Auth/AuthedRoute'
import useToken from '../Auth/useToken'
import Login from "../Auth/Login"
import Register from "../Auth/Register"
import RequestPasswordChange from "../Auth/RequestChangePassword"

//Profile
import Profile from "../profile/Profile"

//notification
import Notification from '../notification/notification'

//notification
import Community from '../community/community'

//error page
import PageNotFound from '../error/pageNotFound'

function AppRouter() {

	const location = useLocation();
	console.log(location.pathname)
	const profileLocation = location.pathname.includes('user') && !location.pathname.includes('follow')
	const trendDisplay= location.pathname.includes('home') || location.pathname.includes('explore') 
	const sideBarDisplay = location.pathname === "/settings" || location.pathname === "/profile" || location.pathname === "/notifications" || location.pathname === "/community" || location.pathname === "/home" 

	// console.log(sideBarDisplay)
	// console.log(location.pathname)
	// console.log(followerLocation)
	// console.log(followingLocation)
	

	const { token, removeToken, setToken } = useToken();

	const [appState, setAppState] = useState({
		loading: false,
	});

	const [userInfo, setUserInfo] = useState(
		{
		uid:null,
		cuid:null,
		currentUser:'',
		userLinks:'',
		}
	);

	return (
		<UserContext.Provider value={{token, userInfo, appState, setAppState, setUserInfo, removeToken, setToken}}>
			<Header />
			<div className='App'>
				{sideBarDisplay && <Sidebar/> }
				{/* {console.log(userInfo.uzer)} */}
				{console.log(location.pathname)}
				{/* username: {userInfo.currentUser} */}
				<Routes>
					<Route exact path="/login" element={<Login/>}></Route>
					<Route exact path="/register" element={<Register/>}></Route>
					<Route exact path="/" element={<Base />}></Route> 
					<Route exact path="/notifications" element= {
								<AuthedRoute >
									<Notification />
								</AuthedRoute>
								} />
					<Route exact path="/community" element={
								<AuthedRoute >
									<Community />
								</AuthedRoute>
								} /> 
					<Route exact path="/accounts/password/reset/" element={<RequestPasswordChange/>}></Route>
					<Route exact path="/explore" element={
								<AuthedRoute >
									<Explore/>
								</AuthedRoute>
								} />
					<Route exact path="/home" 
						element={
								<AuthedRoute >
									<Home />
								</AuthedRoute>
								} />
					<Route exact path="/settings" 
						element={
								<AuthedRoute >
									<Settings />
								</AuthedRoute>
								} />
					{profileLocation &&
						<Route exact path={`${location.pathname}`} element={<Profile />} />
						}
					<Route path='*' element={<PageNotFound />}/>
				</Routes> 				
				{(token && trendDisplay)  && <Trend />}
				{/* <Footer /> */}
			</div>
		</UserContext.Provider>
	)
}

export default AppRouter;
