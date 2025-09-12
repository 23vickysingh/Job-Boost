import React from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { AlertCircle, FileText, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface ProfileIncompleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  needsResume: boolean;
  needsPreferences: boolean;
}

const ProfileIncompleteModal: React.FC<ProfileIncompleteModalProps> = ({
  isOpen,
  onClose,
  needsResume,
  needsPreferences,
}) => {
  const navigate = useNavigate();

  const handleUploadResume = () => {
    onClose();
    navigate('/resume-upload');
  };

  const handleSetPreferences = () => {
    onClose();
    navigate('/job-preferences');
  };

  const getMissingItems = () => {
    const items = [];
    if (needsResume) items.push('Resume');
    if (needsPreferences) items.push('Job Preferences');
    return items;
  };

  const getModalContent = () => {
    const missingItems = getMissingItems();
    
    if (missingItems.length === 2) {
      return {
        title: "Complete Your Profile",
        description: "To get personalized job matches, please upload your resume and set your job preferences.",
        actions: (
          <div className="flex flex-col sm:flex-row gap-3 w-full">
            <Button onClick={handleUploadResume} className="flex-1 min-w-0">
              <FileText className="mr-2 h-4 w-4 flex-shrink-0" />
              <span className="truncate">Upload Resume</span>
            </Button>
            <Button onClick={handleSetPreferences} variant="outline" className="flex-1 min-w-0">
              <Settings className="mr-2 h-4 w-4 flex-shrink-0" />
              <span className="truncate">Set Preferences</span>
            </Button>
          </div>
        )
      };
    } else if (needsResume) {
      return {
        title: "Resume Required",
        description: "Please upload your resume to get personalized job matches based on your skills and experience.",
        actions: (
          <Button onClick={handleUploadResume} className="w-full">
            <FileText className="mr-2 h-4 w-4" />
            Upload Resume
          </Button>
        )
      };
    } else {
      return {
        title: "Job Preferences Required",
        description: "Please set your job preferences to help us find the most relevant opportunities for you.",
        actions: (
          <Button onClick={handleSetPreferences} className="w-full">
            <Settings className="mr-2 h-4 w-4" />
            Set Job Preferences
          </Button>
        )
      };
    }
  };

  const content = getModalContent();

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-lg lg:max-w-xl">
        <DialogHeader>
          <DialogTitle className="flex items-center text-xl font-semibold">
            <AlertCircle className="mr-3 h-6 w-6 text-orange-500" />
            {content.title}
          </DialogTitle>
          <DialogDescription className="pt-2">
            {content.description}
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <h4 className="font-medium text-orange-800 mb-2">Missing Information:</h4>
            <ul className="space-y-1">
              {needsResume && (
                <li className="flex items-center text-orange-700">
                  <FileText className="mr-2 h-4 w-4" />
                  Resume Upload
                </li>
              )}
              {needsPreferences && (
                <li className="flex items-center text-orange-700">
                  <Settings className="mr-2 h-4 w-4" />
                  Job Preferences
                </li>
              )}
            </ul>
          </div>
        </div>

        <DialogFooter className="flex flex-col gap-3 w-full">
          <div className="w-full">
            {content.actions}
          </div>
          <Button 
            variant="ghost" 
            onClick={onClose}
            className="w-full"
          >
            Not Now
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ProfileIncompleteModal;
