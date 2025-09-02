
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Award, Clock, Globe, Briefcase } from "lucide-react";
import Navbar from '@/components/Navbar';
import { useAuth } from "@/contexts/AuthContext";

const About = () => {
  const { token } = useAuth();

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <section className="hero-gradient py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white animate-fade-up">About JobBoost</h1>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto animate-fade-up" style={{ animationDelay: "0.2s" }}>
              Revolutionizing the job application process through automation and AI-powered job matching.
            </p>
          </div>
          
          <div className="mt-20 grid md:grid-cols-2 gap-16 items-center">
            <div className="animate-fade-in" style={{ animationDelay: "0.4s" }}>
              <img 
                src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" 
                alt="Team working together" 
                className="rounded-xl shadow-xl"
              />
            </div>
            <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.6s" }}>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Our Mission</h2>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                At JobBoost, we believe the job search process is broken. Talented people spend countless hours searching and applying for jobs, often with little feedback or results.
              </p>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                Our mission is to empower job seekers by automating the tedious parts of job hunting, so they can focus on what matters most: preparing for interviews and improving their skills.
              </p>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                We're using advanced AI technology to match candidates with relevant positions, automate applications, and provide insights that help them land their dream jobs faster.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-slate-900">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Why Choose JobBoost</h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              We're transforming the job search experience with cutting-edge technology and a user-centered approach.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full w-fit mb-4">
                <Clock className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Save Time</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Automate your job search and application process, saving hours each week.
              </p>
            </div>
            
            <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full w-fit mb-4">
                <Award className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Better Matches</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Our AI algorithm finds jobs that truly match your skills and career goals.
              </p>
            </div>
            
            <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full w-fit mb-4">
                <Globe className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Global Reach</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Access job opportunities across multiple countries and job boards.
              </p>
            </div>
            
            <div className="bg-white dark:bg-slate-800 rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-full w-fit mb-4">
                <Briefcase className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Career Insights</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Get data-driven insights on how to improve your job search strategy.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Our Story</h2>
          </div>
          
          <div className="prose prose-lg dark:prose-invert max-w-4xl mx-auto">
            <p>
              JobBoost was founded in 2023 by a team of tech professionals who were frustrated with the inefficiencies of the traditional job application process. After experiencing firsthand the challenges of job hunting in a competitive market, they decided to build a solution.
            </p>
            <p>
              The founding team combined their expertise in artificial intelligence, web development, and recruitment to create a platform that would revolutionize how people find and apply for jobs.
            </p>
            <p>
              Since our launch, we've helped thousands of job seekers streamline their job search, resulting in more interviews and better job offers. Our platform continuously evolves based on user feedback and the latest developments in AI technology.
            </p>
            <p>
              Today, JobBoost is trusted by job seekers across industries, from recent graduates to experienced professionals looking for their next career move.
            </p>
          </div>
        </div>
      </section>
      
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-blue-600 dark:bg-blue-700 text-white">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-3xl font-bold">Ready to Transform Your Job Search?</h2>
          <p className="mt-4 text-xl max-w-3xl mx-auto text-white/90">
            Join thousands of job seekers who have already discovered the power of automated job applications.
          </p>
          <div className="mt-10">
            <Link to={token ? "/dashboard" : "/signup"}>
              <Button className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-6">
                {token ? "Go to your Profile" : "Get Started Now"}
              </Button>
            </Link>
          </div>
        </div>
      </section>
      
      {/* Footer (reusing the same as on the landing page) */}
      <footer className="bg-gray-100 dark:bg-slate-900 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-8 md:mb-0">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                JobBoost
              </div>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                Your smart job-hunting assistant
              </p>
            </div>
            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-8">
              <div className="text-center md:text-left">
                <h3 className="font-medium text-gray-900 dark:text-white">Quick Links</h3>
                <ul className="mt-2 space-y-2">
                  <li>
                    <Link to="/about" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      About
                    </Link>
                  </li>
                  <li>
                    <Link to="/faq" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      FAQ
                    </Link>
                  </li>
                  <li>
                    <Link to="/contact" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      Contact
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800 text-center">
            <p className="text-gray-600 dark:text-gray-300">
              &copy; {new Date().getFullYear()} JobBoost. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default About;
