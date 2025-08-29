
import Link from "next/link";


export default function Header() {
    return (
	<header>
		<a href="/home" className = "logo">Deception Detector</a>
		<ul>
			<li><a href="">About</a></li>
			<li><a href="">Help</a></li>
		</ul>
	</header>
    )

}

