import React from 'react';
import {Link} from "react-router-dom";


const Home = () => {

 return (

   <div className="navbar">
        <Link to="/purchase">
            <button>Make a Purchase</button></Link>
       <Link to="/purchasehistory">
            <button>See my Purchase History</button></Link>


   </div>
 );
};

export default Home;