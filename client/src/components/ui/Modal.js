import React from "react";
import DatePicker from "@/components/ui/DatePicker";
// import { Calendar } from '@/components/ui/calendar'
import { Button } from "@/components/ui/button";
// import { Label } from "@/components/ui/label"
// import  { useRouter } from 'next/navigation'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

const page = () => {
  return (
    <div>
      <Dialog className="bg-blue-300">
        <DialogTrigger asChild>
          <svg
            width="50"
            height="50"
            viewBox="0 0 28 28"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="bg-blue-500 rounded-full fixed right-12 bottom-10 shadow-2xl shadow-blue-500/50 max-md:right-6"
          >
            <path
              d="M20.9999 15.1643H15.1666V20.9977C15.1666 21.3071 15.0437 21.6038 14.8249 21.8226C14.6061 22.0414 14.3093 22.1643 13.9999 22.1643C13.6905 22.1643 13.3938 22.0414 13.175 21.8226C12.9562 21.6038 12.8333 21.3071 12.8333 20.9977V15.1643H6.99992C6.6905 15.1643 6.39375 15.0414 6.17496 14.8226C5.95617 14.6038 5.83325 14.3071 5.83325 13.9977C5.83325 13.6882 5.95617 13.3915 6.17496 13.1727C6.39375 12.9539 6.6905 12.831 6.99992 12.831H12.8333V6.99766C12.8333 6.68824 12.9562 6.39149 13.175 6.1727C13.3938 5.95391 13.6905 5.83099 13.9999 5.83099C14.3093 5.83099 14.6061 5.95391 14.8249 6.1727C15.0437 6.39149 15.1666 6.68824 15.1666 6.99766V12.831H20.9999C21.3093 12.831 21.6061 12.9539 21.8249 13.1727C22.0437 13.3915 22.1666 13.6882 22.1666 13.9977C22.1666 14.3071 22.0437 14.6038 21.8249 14.8226C21.6061 15.0414 21.3093 15.1643 20.9999 15.1643Z"
              fill="white"
            />
          </svg>
        </DialogTrigger>
        <DialogContent className="sm:max-w-fit max-md:w-fit max-w-md:h-fit bg-white">
          <DialogHeader className="w-fit m-auto">
            <DatePicker />
          </DialogHeader>

          {/* <DialogFooter> */}
          {/* <Button type="submit">Save changes</Button> */}
          {/* </DialogFooter> */}
        </DialogContent>
      </Dialog>
      {/* <Calendar/> */}
    </div>
  );
};

export default page;
