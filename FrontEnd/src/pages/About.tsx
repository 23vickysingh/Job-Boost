
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
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 animate-fade-up">About JobBoost</h1>
            <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto animate-fade-up" style={{ animationDelay: "0.2s" }}>
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
              <h2 className="text-3xl font-bold text-gray-900">Our Mission</h2>
              <p className="text-lg text-gray-600">
                The current job search process is a grind. You're a talented professional, but you're wasting time and energy on a broken system—endlessly searching, scanning, and applying without meaningful results.
              </p>
              <p className="text-lg text-gray-600">
                I'm here to fix that. My goal is to empower job seekers by turning a tedious process into a strategic one. I use powerful AI to find your next role for you, cutting through the noise to deliver the most relevant opportunities and actionable insights.
              </p>
              <p className="text-lg text-gray-600">
                Imagine spending your time preparing for interviews and advancing your skills, not chasing down job listings. That's the future of job hunting—and I'm building it.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900">Why Choose JobBoost</h2>
            <p className="mt-4 text-lg text-gray-600 max-w-3xl mx-auto">
              We're transforming the job search experience with cutting-edge technology and a user-centered approach.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 rounded-full w-fit mb-4">
                <Clock className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Save Time</h3>
              <p className="text-gray-600">
                Automate your job search and application process, saving hours each week.
              </p>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 rounded-full w-fit mb-4">
                <Award className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Better Matches</h3>
              <p className="text-gray-600">
                Our AI algorithm finds jobs that truly match your skills and career goals.
              </p>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 rounded-full w-fit mb-4">
                <Globe className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Global Reach</h3>
              <p className="text-gray-600">
                Access job opportunities across multiple countries and job boards.
              </p>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-md">
              <div className="p-3 bg-blue-100 rounded-full w-fit mb-4">
                <Briefcase className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Career Insights</h3>
              <p className="text-gray-600">
                Get data-driven insights on how to improve your job search strategy.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900">Our Story</h2>
          </div>
          
          <div className="prose prose-lg max-w-4xl mx-auto">
            <p>
              Like many of you, I've been there—stuck in the endless cycle of job searching. I was frustrated with the hours spent on different sites, the repetitive applications, and the lack of feedback. The traditional process felt broken, and I knew there had to be a better way.
            </p>
            <p>
              So, in 2025, I decided to build it myself. I poured my experience in tech and my passion for helping people into creating JobBoost. The goal was simple: to automate the tedious parts of job hunting, so talented people like you can focus on what actually matters—honing your skills and preparing for the perfect role.
            </p>
            <p>
              JobBoost uses advanced AI to learn your preferences and find the best opportunities for you, even those you might miss. It's a platform built to be your personal job search assistant, capable of transforming a stressful hunt into a streamlined, strategic search.
            </p>
            <p>
              While JobBoost is new, it's a powerful tool designed to give you a real advantage in a competitive market. My mission is to empower you to find your next great career move faster and with less effort.
            </p>
          </div>
        </div>
      </section>
      
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-blue-600 text-white">
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
      <footer className="bg-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-8 md:mb-0">
              <div className="text-2xl font-bold text-blue-600">
                JobBoost
              </div>
              <p className="mt-2 text-gray-600">
                Your smart job-hunting assistant
              </p>
            </div>
            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-8">
              <div className="text-center md:text-left">
                <h3 className="font-medium text-gray-900">Quick Links</h3>
                <ul className="mt-2 space-y-2">
                  <li>
                    <Link to="/about" className="text-gray-600 hover:text-blue-600">
                      About
                    </Link>
                  </li>
                  <li>
                    <Link to="/faq" className="text-gray-600 hover:text-blue-600">
                      FAQ
                    </Link>
                  </li>
                  <li>
                    <Link to="/contact" className="text-gray-600 hover:text-blue-600">
                      Contact
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-200 text-center">
            <p className="text-gray-600">
              &copy; {new Date().getFullYear()} JobBoost. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default About;
