
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

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
