
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

interface AuthFormProps {
  type: 'signin' | 'signup';
  onSubmit: (e: React.FormEvent) => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ type, onSubmit }) => {
  const isSignIn = type === 'signin';

  return (
    <div className="glass-card w-full max-w-md mx-auto rounded-xl p-8 shadow-xl">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold">
          {isSignIn ? 'Sign In to JobBoost' : 'Create Your JobBoost Account'}
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mt-2">
          {isSignIn 
            ? 'Enter your credentials to access your account' 
            : 'Start your automated job hunting journey today'}
        </p>
      </div>

      <form onSubmit={onSubmit} className="space-y-4">

        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" name='email' type="email" placeholder="your@email.com" required />
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            {isSignIn && (
              <Link 
                to="/forgot-password" 
                className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
              >
                Forgot Password?
              </Link>
            )}
          </div>
          <Input id="password" name='password' type="password" required />
        </div>

        {!isSignIn && (
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input id="confirmPassword" name='confirm' type="password" required />
          </div>
        )}

        <Button type="submit" className="w-full">
          {isSignIn ? 'Sign In' : 'Sign Up'}
        </Button>
      </form>

      <div className="mt-6">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <Separator />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">
              Or continue with
            </span>
          </div>
        </div>

        <div className="mt-4 flex gap-2">
          <Button 
            variant="outline" 
            className="w-full"
            onClick={(e) => e.preventDefault()}
          >
            <svg className="mr-2 h-4 w-4" viewBox="0 0 48 48" fill="none">
              <path
                d="M47.532 24.5528c0-1.6264-.1635-3.2032-.4691-4.7347h-22.26v8.9482h12.7305c-.5487 2.9658-2.2183 5.4752-4.7209 7.1628v5.9578h7.6416c4.4638-4.1149 7.0384-10.1695 7.0384-17.3441z"
                fill="#4285F4"
              />
              <path
                d="M24.8032 48c6.3849 0 11.7403-2.1143 15.6622-5.7315l-7.6416-5.9578c-2.1189 1.4201-4.8302 2.2567-8.0206 2.2567-6.1651 0-11.3992-4.1567-13.2627-9.7451H3.69922v6.1451C7.61707 42.9168 15.5598 48 24.8032 48z"
                fill="#34A853"
              />
              <path
                d="M11.5405 28.8235C11.0166 27.4202 10.7188 25.9238 10.7188 24.375c0-1.5487.3032-3.045.8216-4.4485V13.781H3.69922C2.44992 16.9883 1.71875 20.4017 1.71875 24c0 3.5983.73117 7.0117 1.98047 10.219l7.84128-5.3955z"
                fill="#FBBC05"
              />
              <path
                d="M24.8033 9.03051c3.4749 0 6.593 1.19331 9.0409 3.5353l6.7679-6.77169C36.3481 2.1243 31.0875 0 24.8033 0 15.5599 0 7.61701 5.08308 3.69922 13.781l7.84118 5.3955c1.8635-5.58851 7.0976-9.74559 13.2629-9.74559z"
                fill="#EA4335"
              />
            </svg>
            Google
          </Button>
        </div>
      </div>

      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600 dark:text-gray-300">
          {isSignIn ? "Don't have an account?" : "Already have an account?"}
          <Link
            to={isSignIn ? "/signup" : "/signin"}
            className="ml-1 text-blue-600 dark:text-blue-400 hover:underline"
          >
            {isSignIn ? "Sign up" : "Sign in"}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default AuthForm;
