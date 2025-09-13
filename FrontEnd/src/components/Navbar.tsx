
import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogCancel,
  AlertDialogAction,
} from "@/components/ui/alert-dialog";
import { Menu, X } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

const Navbar = () => {
        const [isMenuOpen, setIsMenuOpen] = useState(false);
        const location = useLocation();
        const { token, logout } = useAuth();

	const toggleMenu = () => {
		setIsMenuOpen(!isMenuOpen);
	};

	return (
		<nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div className="flex justify-between items-center h-16">
					<div className="flex items-center">
						<Link
							to="/"
							className="flex items-center space-x-2 text-xl font-bold text-blue-600"
						>
							<span className="text-2xl">JobBoost</span>
						</Link>
					</div>
					<div className="hidden md:flex md:items-center md:space-x-6">
						<div className="flex items-center space-x-6">
							<Link
								to="/"
								className={`text-gray-600 hover:text-blue-600 ${location.pathname === "/"
										? "text-blue-600"
										: ""
									}`}
							>
								Home
							</Link>
							<Link
								to="/about"
								className={`text-gray-600 hover:text-blue-600 ${location.pathname === "/about"
										? "text-blue-600"
										: ""
									}`}
							>
								About
							</Link>
							<Link
								to="/faq"
								className={`text-gray-600 hover:text-blue-600 ${location.pathname === "/faq"
										? "text-blue-600"
										: ""
									}`}
							>
								FAQ
							</Link>
                                                        {token ? (
                                                                <>
                                                                        <Link
                                                                                to="/dashboard"
                                                                                className={`text-gray-600 hover:text-blue-600 ${location.pathname === "/dashboard" ? "text-blue-600" : ""}`}
                                                                        >
                                                                                Dashboard
                                                                        </Link>
<AlertDialog>
        <AlertDialogTrigger asChild>
                <Button variant="outline" className="mr-2">
                        Sign Out
                </Button>
        </AlertDialogTrigger>
        <AlertDialogContent>
                <AlertDialogHeader>
                        <AlertDialogTitle>Sign Out</AlertDialogTitle>
                        <AlertDialogDescription>
                                Are you sure you want to sign out?
                        </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction onClick={logout}>Sign Out</AlertDialogAction>
                </AlertDialogFooter>
        </AlertDialogContent>
</AlertDialog>
                                                                </>
                                                        ) : (
                                                                <>
                                                                        <Link to="/signin">
                                                                                <Button variant="outline" className="mr-2">
                                                                                        Sign In
                                                                                </Button>
                                                                        </Link>
                                                                        <Link to="/signup">
                                                                                <Button>Sign Up</Button>
                                                                        </Link>
                                                                </>
                                                        )}
						</div>
					</div>
					<div className="md:hidden flex items-center">
						<button
							onClick={toggleMenu}
							className="p-2 rounded-full bg-gray-100 text-gray-800"
							aria-label="Open menu"
						>
							{isMenuOpen ? <X size={18} /> : <Menu size={18} />}
						</button>
					</div>
				</div>
			</div>
			{/* Mobile menu */}
			{isMenuOpen && (
				<div className="md:hidden">
					<div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white shadow-lg animate-fade-down">
						<Link
							to="/about"
							className={`block px-3 py-2 rounded-md text-base font-medium ${location.pathname === "/about"
									? "text-blue-600 bg-gray-100"
									: "text-gray-700 hover:bg-gray-100"
								}`}
							onClick={toggleMenu}
						>
							About
						</Link>
                                                {token ? (
                                                        <>
                                                                <Link
                                                                        to="/dashboard"
                                                                        className={`block px-3 py-2 rounded-md text-base font-medium ${location.pathname === "/dashboard" ? "text-blue-600 bg-gray-100" : "text-gray-700 hover:bg-gray-100"}`}
                                                                        onClick={toggleMenu}
                                                                >
                                                                        Dashboard
                                                                </Link>
                                                                <AlertDialog>
                                                                        <AlertDialogTrigger asChild>
                                                                                <button
                                                                                        className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100"
                                                                                >
                                                                                        Sign Out
                                                                                </button>
                                                                        </AlertDialogTrigger>
                                                                        <AlertDialogContent>
                                                                                <AlertDialogHeader>
                                                                                        <AlertDialogTitle>Sign Out</AlertDialogTitle>
                                                                                        <AlertDialogDescription>
                                                                                                Are you sure you want to sign out?
                                                                                        </AlertDialogDescription>
                                                                                </AlertDialogHeader>
                                                                                <AlertDialogFooter>
                                                                                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                                                                                        <AlertDialogAction onClick={() => { logout(); toggleMenu(); }}>Sign Out</AlertDialogAction>
                                                                                </AlertDialogFooter>
                                                                        </AlertDialogContent>
                                                                </AlertDialog>
                                                        </>
                                                ) : (
                                                        <>
                                                                <Link
                                                                        to="/signin"
                                                                        className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100"
                                                                        onClick={toggleMenu}
                                                                >
                                                                        Sign In
                                                                </Link>
                                                                <Link
                                                                        to="/signup"
                                                                        className="block px-3 py-2 rounded-md text-base font-medium bg-blue-600 text-white hover:bg-blue-700"
                                                                        onClick={toggleMenu}
                                                                >
                                                                        Sign Up
                                                                </Link>
                                                        </>
                                                )}
					</div>
				</div>
			)}
		</nav>
	);
};

export default Navbar;
