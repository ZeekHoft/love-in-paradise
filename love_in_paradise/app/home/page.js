"use client"
import React, { useEffect, useState } from "react";

function Home() {
    const [message, setMessage] = useState("Loading...")
    const [favorite_dog, setFavorite_Dog] = useState("Loading...")


    useEffect(() => {
        fetch("http://localhost:8080/api/home")
            .then((response) => response.json())
            .then((data) => {
                // console.log(data)
                setMessage(data.message);
                setFavorite_Dog(data.favorite_dog);

            })

    }, [])
    return (


        <div>{message} {favorite_dog}


        </div>

        // <div className="h-screen flex items-center justify-center bg-black">
        //     <input
        //         className="border border-gray-400 rounded-md p-2 focus:border-blue-500 outline-none"
        //         placeholder="Enter News"
        //     />
        // </div>


    );
}
export default Home;