
import Link from "next/link";


export default function Header() {
    return (
        <header>
            <nav>
                <ul>
                    <li>
                        <Link href="/home" className="hover:text-gray-300">
                            Home
                        </Link>
                    </li>
                    <li>
                        <Link href="/about" className="hover:text-gray-300">
                            About
                        </Link>
                    </li>
                </ul>
            </nav>
        </header>
    )

}

