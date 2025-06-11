
import React from 'react';
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import PreferencesSection from './PreferencesSection';

interface PreferencesData {
  roles: string[];
  locations: string[];
  workMode: string;
  skills: string[];
  experienceLevel: string;
  salaryExpectation: string;
}

interface EditPreferencesFormProps {
  preferences: PreferencesData;
  onPreferencesChange: (preferences: PreferencesData) => void;
  newRole: string;
  setNewRole: (role: string) => void;
  newLocation: string;
  setNewLocation: (location: string) => void;
  newSkill: string;
  setNewSkill: (skill: string) => void;
  addRole: () => void;
  removeRole: (role: string) => void;
  addLocation: () => void;
  removeLocation: (location: string) => void;
  addSkill: () => void;
  removeSkill: (skill: string) => void;
}

const EditPreferencesForm: React.FC<EditPreferencesFormProps> = ({
  preferences,
  onPreferencesChange,
  newRole,
  setNewRole,
  newLocation,
  setNewLocation,
  newSkill,
  setNewSkill,
  addRole,
  removeRole,
  addLocation,
  removeLocation,
  addSkill,
  removeSkill
}) => {
  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-4">
          <div>
            <Label htmlFor="workMode">Work Mode</Label>
            <select 
              id="workMode"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              value={preferences.workMode}
              onChange={(e) => onPreferencesChange({...preferences, workMode: e.target.value})}
            >
              <option value="Remote">Remote</option>
              <option value="On-site">On-site</option>
              <option value="Hybrid">Hybrid</option>
            </select>
          </div>
          
          <div>
            <Label htmlFor="experienceLevel">Experience Level</Label>
            <select 
              id="experienceLevel"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              value={preferences.experienceLevel}
              onChange={(e) => onPreferencesChange({...preferences, experienceLevel: e.target.value})}
            >
              <option value="Entry-Level">Entry-Level</option>
              <option value="Mid-Level">Mid-Level</option>
              <option value="Senior-Level">Senior-Level</option>
              <option value="Lead/Manager">Lead/Manager</option>
            </select>
          </div>
          
          <div>
            <Label htmlFor="salary">Salary Expectation</Label>
            <Input 
              id="salary"
              value={preferences.salaryExpectation}
              onChange={(e) => onPreferencesChange({...preferences, salaryExpectation: e.target.value})}
            />
          </div>
        </div>
        
        <div className="space-y-4">
          <PreferencesSection
            title="Seeking Roles"
            items={preferences.roles}
            onRemove={removeRole}
            onAdd={(role) => {
              setNewRole(role);
              addRole();
            }}
            placeholder="Add a role"
            badgeVariant="secondary"
          />
          
          <PreferencesSection
            title="Locations"
            items={preferences.locations}
            onRemove={removeLocation}
            onAdd={(location) => {
              setNewLocation(location);
              addLocation();
            }}
            placeholder="Add a location"
            badgeVariant="outline"
          />
        </div>
      </div>
      
      <PreferencesSection
        title="Skills"
        items={preferences.skills}
        onRemove={removeSkill}
        onAdd={(skill) => {
          setNewSkill(skill);
          addSkill();
        }}
        placeholder="Add a skill"
        badgeVariant="secondary"
        badgeClassName="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
      />
    </div>
  );
};

export default EditPreferencesForm;
