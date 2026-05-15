<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class GradientController extends AbstractController
{
    #[Route('/gradient', name: 'app_gradient')]
    public function index(Request $request): Response
    {
        $result    = null;
        $error     = null;
        $chartData = null;
        $iterations = [];

        if ($request->isMethod('POST')) {
            try {
                $x0    = (float) $request->request->get('x0', 0);
                $delta = (float) $request->request->get('delta', 0.1);
                $maxIter = (int) $request->request->get('maxIter', 50);
                $tol   = 1e-6;

                // Coefficients du polynôme J(x) = a2*x^2 + a1*x + a0
                $a2 = (float) $request->request->get('a2', 1);
                $a1 = (float) $request->request->get('a1', 0);
                $a0 = (float) $request->request->get('a0', 0);

                if ($a2 <= 0) throw new \Exception('Le coefficient a₂ doit être > 0 pour avoir un minimum.');
                if ($delta <= 0 || $delta >= 2) throw new \Exception('Le pas δ doit être dans ]0, 2[.');

                $x = $x0;
                $iterations[] = ['k' => 0, 'x' => round($x, 6), 'grad' => round(2*$a2*$x + $a1, 6), 'J' => round($a2*$x*$x + $a1*$x + $a0, 6)];

                for ($k = 1; $k <= $maxIter; $k++) {
                    $grad = 2 * $a2 * $x + $a1; // J'(x) = 2*a2*x + a1
                    $xNew = $x - $delta * $grad;

                    $iterations[] = [
                        'k'    => $k,
                        'x'    => round($xNew, 6),
                        'grad' => round(2*$a2*$xNew + $a1, 6),
                        'J'    => round($a2*$xNew*$xNew + $a1*$xNew + $a0, 6),
                    ];

                    if (abs($xNew - $x) < $tol) { $x = $xNew; break; }
                    $x = $xNew;
                }

                $xStar = -$a1 / (2 * $a2); // minimum exact
                $result = [
                    'x_final' => round($x, 8),
                    'x_star'  => round($xStar, 8),
                    'J_min'   => round($a2*$xStar*$xStar + $a1*$xStar + $a0, 8),
                    'nb_iter' => count($iterations) - 1,
                ];

                // Données graphique
                $chartData = $this->prepareChart($a2, $a1, $a0, $iterations);

            } catch (\Exception $e) {
                $error = $e->getMessage();
            }
        }

        return $this->render('gradient/index.html.twig', [
            'result'     => $result,
            'error'      => $error,
            'iterations' => $iterations,
            'chartData'  => $chartData,
        ]);
    }

    private function prepareChart(float $a2, float $a1, float $a0, array $iterations): array
    {
        $xs = array_column($iterations, 'x');
        $xMin = min($xs); $xMax = max($xs);
        $range = max($xMax - $xMin, 2);
        $extMin = $xMin - $range * 0.5;
        $extMax = $xMax + $range * 0.5;

        $curveX = []; $curveY = [];
        for ($i = 0; $i <= 200; $i++) {
            $xi = $extMin + ($extMax - $extMin) * ($i / 200);
            $curveX[] = round($xi, 4);
            $curveY[] = round($a2*$xi*$xi + $a1*$xi + $a0, 6);
        }

        $points = array_map(fn($it) => ['x' => $it['x'], 'y' => $it['J']], $iterations);

        return ['curveX' => $curveX, 'curveY' => $curveY, 'points' => $points];
    }
}
