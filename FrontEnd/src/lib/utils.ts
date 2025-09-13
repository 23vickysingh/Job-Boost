import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}


// without cn() conflicts can occur, the application can be unpredictable

// twMerge merges the classes intelligently, respecting tailwind's rules