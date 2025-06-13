"use client"


export default function Home() {
    return (


        <form action="/api/submit" method="post">
            <label htmlFor="news">News:</label>
            <input type="text" id="news" name="news" required />



            <button type="submit">Submit</button>
        </form>


    );
}
