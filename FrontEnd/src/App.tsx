
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import React from 'react'; // Add explicit React import
import Index from "./pages/Index";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import ForgotPassword from "./pages/ForgotPassword";
import About from "./pages/About";
import Dashboard from "./pages/Dashboard";
import ResumeUpload from "./pages/ResumeUpload";
import PersonalInfo from "./pages/PersonalInfo";
import JobPreferences from "./pages/JobPreferences";
import UpdatePersonalInfo from "./pages/UpdatePersonalInfo";
import UpdateJobPreferences from "./pages/UpdateJobPreferences";
import NotFound from "./pages/NotFound";
import FAQ from "./pages/FAQ";
import Contact from "./pages/Contact";
import ProtectedRoute from "@/components/ProtectedRoute";

// Create the client outside of the component
const queryClient = new QueryClient();

const App = () => {
  return (
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/about" element={<About />} />
              <Route path="/faq" element={<FAQ />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/personal-info" element={
                <ProtectedRoute>
                  <JobPreferences />
                </ProtectedRoute>
              } />
              <Route path="/job-preferences" element={
                <ProtectedRoute>
                  <JobPreferences />
                </ProtectedRoute>
              } />
              <Route path="/update-profile" element={
                <ProtectedRoute>
                  <UpdateJobPreferences />
                </ProtectedRoute>
              } />
              <Route path="/update-job-preferences" element={
                <ProtectedRoute>
                  <UpdateJobPreferences />
                </ProtectedRoute>
              } />
              <Route path="/resume-upload" element={
                <ProtectedRoute>
                  <ResumeUpload />
                </ProtectedRoute>
              } />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </QueryClientProvider>
    </React.StrictMode>
  );
};

export default App;
