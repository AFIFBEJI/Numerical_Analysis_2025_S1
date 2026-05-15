<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class LagrangeController extends AbstractController
{
    #[Route('/lagrange', name: 'app_lagrange')]
    public function index(Request $request): Response
    {
        $result      = null;
        $pointsX     = [];
        $pointsY     = [];
        $nbPoints    = 0;
        $polynomial  = null;
        $steps       = null;
        $chartData   = null;
        $error       = null;

        // Étape 1 : récupérer le nombre de points
        if ($request->isMethod('POST') && $request->request->has('nbPoints') && !$request->request->has('x')) {
            $nbPoints = (int) $request->request->get('nbPoints', 0);
        }

        // Étape 2 : calcul
        if ($request->isMethod('POST') && $request->request->has('x') && $request->request->has('y')) {
            $pointsX = $request->request->all('x');
            $pointsY = $request->request->all('y');
            $nbPoints = (int) $request->request->get('nbPoints', count($pointsX));

            $x = array_map('floatval', $pointsX);
            $y = array_map('floatval', $pointsY);
            $n = count($x);

            // Vérifier que les xi sont distincts
            if (count(array_unique($x)) !== $n) {
                $error = "Les valeurs de x doivent être toutes distinctes.";
            } else {
                // --- Calcul correct des βi = yi / ∏(xi - xj), j≠i ---
                $betas = [];
                for ($i = 0; $i < $n; $i++) {
                    $denom = 1.0;
                    for ($j = 0; $j < $n; $j++) {
                        if ($i !== $j) {
                            $denom *= ($x[$i] - $x[$j]);
                        }
                    }
                    $betas[$i] = $y[$i] / $denom;
                }
                $result = array_map([$this, 'formatNum'], $betas);

                // --- Polynôme développé P(x) = Σ βi * ∏(x - xj), j≠i ---
                // On accumule les coefficients du polynôme développé
                $polyCoeffs = array_fill(0, $n, 0.0); // coefficients de x^0 à x^(n-1)

                for ($i = 0; $i < $n; $i++) {
                    // Calculer ∏(x - xj) pour j≠i → polynôme de degré n-1
                    $prod = [1.0]; // commence à 1
                    for ($j = 0; $j < $n; $j++) {
                        if ($i !== $j) {
                            // Multiplier par (x - xj)
                            $newProd = array_fill(0, count($prod) + 1, 0.0);
                            foreach ($prod as $k => $c) {
                                $newProd[$k + 1] += $c;          // x * c
                                $newProd[$k]     -= $x[$j] * $c; // -xj * c
                            }
                            $prod = $newProd;
                        }
                    }
                    // Ajouter βi * prod aux coefficients globaux
                    foreach ($prod as $k => $c) {
                        $polyCoeffs[$k] += $betas[$i] * $c;
                    }
                }

                $polynomial = $this->buildPolynomialString($polyCoeffs);

                // --- Étapes de calcul détaillées ---
                $steps = $this->buildSteps($x, $y, $betas, $n);

                // --- Données graphique ---
                $chartData = $this->prepareChartData($x, $y, $betas);
            }
        }

        return $this->render('lagrange/index.html.twig', [
            'result'     => $result,
            'pointsX'    => $pointsX,
            'pointsY'    => $pointsY,
            'nbPoints'   => $nbPoints,
            'polynomial' => $polynomial,
            'steps'      => $steps,
            'chartData'  => $chartData,
            'error'      => $error,
        ]);
    }

    // -----------------------------------------------------------------------
    // Construit la chaîne du polynôme développé à partir des coefficients
    // -----------------------------------------------------------------------
    private function buildPolynomialString(array $coeffs): string
    {
        $n = count($coeffs);
        $terms = [];

        for ($i = $n - 1; $i >= 0; $i--) {
            $c = $coeffs[$i];
            if (abs($c) < 1e-10) continue;

            $cStr = $this->formatNum(abs($c));
            $sign = $c >= 0 ? '+' : '-';

            if ($i === 0) {
                $term = $cStr;
            } elseif ($i === 1) {
                $term = ($cStr === '1') ? 'x' : $cStr . 'x';
            } else {
                $term = ($cStr === '1') ? "x<sup>$i</sup>" : $cStr . "x<sup>$i</sup>";
            }

            $terms[] = ['sign' => $sign, 'term' => $term];
        }

        if (empty($terms)) return '0';

        $str = ($terms[0]['sign'] === '-' ? '-' : '') . $terms[0]['term'];
        for ($i = 1; $i < count($terms); $i++) {
            $str .= ' ' . $terms[$i]['sign'] . ' ' . $terms[$i]['term'];
        }

        return $str;
    }

    // -----------------------------------------------------------------------
    // Génère les étapes détaillées de calcul
    // -----------------------------------------------------------------------
    private function buildSteps(array $x, array $y, array $betas, int $n): array
    {
        $steps = [];

        // Étape 1 : polynômes de base Li(x)
        for ($i = 0; $i < $n; $i++) {
            $num = '';
            $den = 1.0;
            for ($j = 0; $j < $n; $j++) {
                if ($i !== $j) {
                    $xj = $x[$j];
                    $num .= ($xj == 0) ? '(x)' : ($xj > 0 ? "(x - $xj)" : "(x + " . abs($xj) . ")");
                    $den *= ($x[$i] - $xj);
                }
            }
            $denStr = $this->formatNum($den);
            $steps['Li'][$i] = [
                'num'   => $num,
                'den'   => $denStr,
                'beta'  => $this->formatNum($betas[$i]),
                'yi'    => $this->formatNum($y[$i]),
            ];
        }

        return $steps;
    }

    // -----------------------------------------------------------------------
    // Prépare les données pour Chart.js
    // -----------------------------------------------------------------------
    private function prepareChartData(array $x, array $y, array $betas): array
    {
        $n    = count($x);
        $minX = min($x);
        $maxX = max($x);
        $range = max($maxX - $minX, 1);

        $extMin = $minX - $range * 0.3;
        $extMax = $maxX + $range * 0.3;

        $chartX = [];
        $chartY = [];

        for ($i = 0; $i <= 200; $i++) {
            $xi = $extMin + ($extMax - $extMin) * ($i / 200);
            $chartX[] = round($xi, 4);
            $chartY[] = round($this->evalLagrange($xi, $x, $betas, $n), 6);
        }

        $points = [];
        for ($i = 0; $i < $n; $i++) {
            $points[] = ['x' => $x[$i], 'y' => $y[$i]];
        }

        return ['labels' => $chartX, 'data' => $chartY, 'points' => $points];
    }

    private function evalLagrange(float $xVal, array $x, array $betas, int $n): float
    {
        $result = 0.0;
        for ($i = 0; $i < $n; $i++) {
            $Li = 1.0;
            for ($j = 0; $j < $n; $j++) {
                if ($i !== $j) $Li *= ($xVal - $x[$j]);
            }
            $result += $betas[$i] * $Li;
        }
        return $result;
    }

    private function formatNum(float $v): string
    {
        if (abs($v - round($v)) < 1e-9) return (string)(int)round($v);
        $s = rtrim(rtrim(number_format($v, 6, '.', ''), '0'), '.');
        return $s;
    }
}
