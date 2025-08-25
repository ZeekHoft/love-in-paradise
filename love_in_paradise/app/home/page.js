"use client"
import React, { useEffect, useState } from "react";

function Home() {
    const [message, setMessage] = useState("Loading...")
    const [favorite_dog, setFavorite_Dog] = useState("Loading...")
    const [news, setNews] = useState("Loading")
    //GET

    // useEffect(() => {
    //     fetch("http://localhost:8080/api/home")
    //         .then((response) => response.json())
    //         .then((data) => {
    //             // console.log(data)
    //             setMessage(data.message);
    //             setFavorite_Dog(data.favorite_dog);

    //         })

    // }, [])

    //POST

    const handleSubmit = () => {

        const postData = async (url = '', data = {}) => {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return response.json();
        }
        postData("http://localhost:8080/api/home",
            { name: news })
            .then(data => {
                setMessage(data.message);
                // setFavorite_Dog(data.favorite_dog);

            });
    }



    return (



        <div>


            <input name="news" onChange={(e) => setNews(e.target.value)} />

            <br>
            </br>
            <button onClick={handleSubmit}>Submit</button>

            {/* {favorite_dog} */}


            <br>
            </br>
            <br>
            </br>


            {message}
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