import React from 'react';

interface BreadcrumbsProps {
  steps: string[];
  currentStep: number;
}

const Breadcrumbs: React.FC<BreadcrumbsProps> = ({ steps, currentStep }) => {
  return (
    <div className="w-full px-2 sm:px-0">
      <ol role="list" className="flex items-start">
        {steps.map((step, stepIdx) => {
          const isCompleted = stepIdx < currentStep;
          const isCurrent = stepIdx === currentStep;

          return (
            <React.Fragment key={step}>
              {/* Step: Circle and Text */}
              <li className="flex flex-col items-center flex-shrink-0">
                <div
                  className={`flex h-8 w-8 sm:h-10 sm:w-10 items-center justify-center rounded-full transition-colors duration-300 ${
                    isCompleted
                      ? 'bg-yellow-500'
                      : isCurrent
                      ? 'border-2 border-yellow-500 bg-transparent'
                      : 'border-2 border-gray-600 bg-transparent'
                  }`}
                  aria-current={isCurrent ? 'step' : undefined}
                >
                  {isCompleted ? (
                    <svg className="h-5 w-5 sm:h-6 sm:w-6 text-black" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <span
                      className={`font-semibold text-sm sm:text-base ${
                        isCurrent ? 'text-yellow-500' : 'text-gray-500'
                      }`}
                    >
                      {`0${stepIdx + 1}`}
                    </span>
                  )}
                </div>
                <p
                  className={`mt-2 w-16 sm:w-20 text-center text-xs font-medium ${
                    isCurrent || isCompleted ? 'text-yellow-500' : 'text-gray-500'
                  }`}
                >
                  {step.split(' ').map((word, i) => (
                    <span key={i} className="block leading-tight">{word}</span>
                  ))}
                </p>
              </li>

              {/* Connector for all but the last item */}
              {stepIdx < steps.length - 1 && (
                <div
                  className={`flex-auto border-t-2 transition-colors duration-500 mt-4 sm:mt-5 ${
                    isCompleted ? 'border-yellow-500' : 'border-gray-600'
                  }`}
                  aria-hidden="true"
                />
              )}
            </React.Fragment>
          );
        })}
      </ol>
    </div>
  );
};

export default Breadcrumbs;