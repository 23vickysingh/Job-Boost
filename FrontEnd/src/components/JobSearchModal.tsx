import React, { useEffect, useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Progress } from "@/components/ui/progress";
import { Loader2, Search, Target, Briefcase, TrendingUp } from 'lucide-react';

interface JobSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  searchReason?: string;
}

const JobSearchModal: React.FC<JobSearchModalProps> = ({ 
  isOpen, 
  onClose, 
  searchReason = "first_time" 
}) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    {
      icon: Search,
      title: "Searching Job Listings",
      description: "Scanning thousands of job opportunities"
    },
    {
      icon: Target,
      title: "Analyzing Your Profile",
      description: "Matching your skills and preferences"
    },
    {
      icon: Briefcase,
      title: "Calculating Relevance",
      description: "Finding the best matches for you"
    },
    {
      icon: TrendingUp,
      title: "Finalizing Results",
      description: "Preparing your personalized job matches"
    }
  ];

  useEffect(() => {
    if (!isOpen) {
      setProgress(0);
      setCurrentStep(0);
      return;
    }

    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) return 95; // Don't complete until job search is done
        return prev + Math.random() * 15;
      });
    }, 800);

    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % steps.length);
    }, 3000);

    return () => {
      clearInterval(progressInterval);
      clearInterval(stepInterval);
    };
  }, [isOpen, steps.length]);

  const getSearchMessage = () => {
    switch (searchReason) {
      case "first_time":
        return "Welcome! We're finding the best job opportunities for you.";
      case "outdated":
        return "Refreshing your job matches with the latest opportunities.";
      default:
        return "Finding the best suitable jobs for you...";
    }
  };

  const CurrentStepIcon = steps[currentStep].icon;

  return (
    <Dialog open={isOpen} onOpenChange={() => {}}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center justify-center text-xl font-semibold">
            <Loader2 className="mr-3 h-6 w-6 animate-spin text-blue-600" />
            Job Search in Progress
          </DialogTitle>
          <DialogDescription className="text-center pt-2">
            {getSearchMessage()}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Progress Bar */}
          <div className="space-y-2">
            <Progress value={progress} className="w-full h-2" />
            <p className="text-sm text-gray-500 text-center">
              {Math.round(progress)}% Complete
            </p>
          </div>

          {/* Current Step */}
          <div className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
            <div className="p-2 bg-blue-100 rounded-full">
              <CurrentStepIcon className="h-5 w-5 text-blue-600" />
            </div>
            <div className="flex-1">
              <h4 className="font-medium text-gray-900">
                {steps[currentStep].title}
              </h4>
              <p className="text-sm text-gray-600">
                {steps[currentStep].description}
              </p>
            </div>
          </div>

          {/* Step Indicators */}
          <div className="flex justify-center space-x-2">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`w-2 h-2 rounded-full transition-colors ${
                  index === currentStep ? 'bg-blue-600' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>

          {/* Encouraging Message */}
          <div className="text-center space-y-2">
            <p className="text-sm text-gray-600">
              This may take a few moments while we analyze your profile
            </p>
            <p className="text-xs text-gray-500">
              Please don't close this window
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default JobSearchModal;
