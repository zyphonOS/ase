export default function AseEmblem({ size = 32, className = '' }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Outer geometric eye/seed shape */}
      <path
        d="M32 4C18.7 4 8 18.7 8 32C8 45.3 18.7 60 32 60C45.3 60 56 45.3 56 32C56 18.7 45.3 4 32 4Z"
        stroke="#34D399"
        strokeWidth="1.5"
        fill="none"
      />
      {/* Inner eye arc top */}
      <path
        d="M12 32C12 32 22 16 32 16C42 16 52 32 52 32"
        stroke="#34D399"
        strokeWidth="1"
        fill="none"
      />
      {/* Inner eye arc bottom */}
      <path
        d="M12 32C12 32 22 48 32 48C42 48 52 32 52 32"
        stroke="#34D399"
        strokeWidth="1"
        fill="none"
      />
      {/* Sound wave bars (spoken intent) */}
      <line x1="22" y1="28" x2="22" y2="36" stroke="#34D399" strokeWidth="2" strokeLinecap="round" />
      <line x1="26" y1="25" x2="26" y2="39" stroke="#34D399" strokeWidth="2" strokeLinecap="round" />
      <line x1="30" y1="22" x2="30" y2="42" stroke="#34D399" strokeWidth="2" strokeLinecap="round" />
      {/* Arrow (action) */}
      <path
        d="M35 32L42 32M39 28L43 32L39 36"
        stroke="#34D399"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}
