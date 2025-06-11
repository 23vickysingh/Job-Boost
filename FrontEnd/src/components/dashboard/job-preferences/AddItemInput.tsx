
import React, { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

interface AddItemInputProps {
  placeholder: string;
  onAdd: (item: string) => void;
}

const AddItemInput: React.FC<AddItemInputProps> = ({ placeholder, onAdd }) => {
  const [newItem, setNewItem] = useState("");

  const handleAdd = () => {
    if (newItem.trim()) {
      onAdd(newItem);
      setNewItem("");
    }
  };

  return (
    <div className="flex gap-2">
      <Input 
        placeholder={placeholder} 
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAdd())}
      />
      <Button size="sm" onClick={handleAdd} variant="outline">
        <Plus className="h-4 w-4" />
      </Button>
    </div>
  );
};

export default AddItemInput;
