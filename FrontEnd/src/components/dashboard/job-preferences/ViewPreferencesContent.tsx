
import React from 'react';
import { Badge } from "@/components/ui/badge";

interface PreferencesData {
  roles: string[];
  locations: string[];
  workMode: string;
  skills: string[];
  experienceLevel: string;
  salaryExpectation: string;
}

interface ViewPreferencesContentProps {
  preferences: PreferencesData;
}

const ViewPreferencesContent: React.FC<ViewPreferencesContentProps> = ({ preferences }) => {
  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium mb-2">Seeking Roles</h4>
          <div className="flex flex-wrap gap-2">
            {preferences.roles.map((role, index) => (
              <Badge key={index} variant="secondary">{role}</Badge>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="text-sm font-medium mb-2">Locations</h4>
          <div className="flex flex-wrap gap-2">
            {preferences.locations.map((location, index) => (
              <Badge key={index} variant="outline">{location}</Badge>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="text-sm font-medium mb-2">Work Mode</h4>
          <p className="text-sm text-gray-600 dark:text-gray-300">{preferences.workMode}</p>
        </div>
      </div>
      
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium mb-2">Skills</h4>
          <div className="flex flex-wrap gap-2">
            {preferences.skills.map((skill, index) => (
              <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                {skill}
              </Badge>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="text-sm font-medium mb-2">Experience Level</h4>
          <p className="text-sm text-gray-600 dark:text-gray-300">{preferences.experienceLevel}</p>
        </div>
        
        <div>
          <h4 className="text-sm font-medium mb-2">Salary Expectation</h4>
          <p className="text-sm text-gray-600 dark:text-gray-300">{preferences.salaryExpectation}</p>
        </div>
      </div>
    </div>
  );
};

export default ViewPreferencesContent;
